#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mama_baby_math.py

A tiny, trainable math Transformer with:
- Mother Math mode: arithmetic-only (add/sub/mul/div/mix) with curriculum on digits
- Baby Math mode: developmental curriculum:
    compare dots -> dots-to-number -> arithmetic digits

Features:
- Infinite programmatic data generation (teacher/answer is always exact)
- Curriculum learning
- OOD digit generalization evaluation for arithmetic
- Task-wise evaluation for baby stages

Usage:
  python mama_baby_math.py --mode baby --op add --train_steps 40000 --device cuda
  python mama_baby_math.py --mode mother --op mix --train_steps 80000 --device cuda
"""

import math
import random
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Dict

import torch
import torch.nn as nn
import torch.nn.functional as F


def set_seed(seed: int):
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


class CharTokenizer:
    def __init__(self):
        self.PAD = "<pad>"
        self.BOS = "<bos>"
        self.EOS = "<eos>"

        # Character-level vocabulary
        self.tokens = [
            self.PAD, self.BOS, self.EOS,
            "0","1","2","3","4","5","6","7","8","9",
            "+","-","*","/","=","\n",
            "•","?","L","R",">"
        ]
        self.stoi = {t: i for i, t in enumerate(self.tokens)}
        self.itos = {i: t for t, i in self.stoi.items()}

    @property
    def pad_id(self): return self.stoi[self.PAD]

    @property
    def bos_id(self): return self.stoi[self.BOS]

    @property
    def eos_id(self): return self.stoi[self.EOS]

    def encode(self, s: str, add_bos_eos: bool = True) -> List[int]:
        ids = []
        for ch in s:
            if ch not in self.stoi:
                raise ValueError(f"Unknown char: {repr(ch)}")
            ids.append(self.stoi[ch])
        if add_bos_eos:
            return [self.bos_id] + ids + [self.eos_id]
        return ids

    def decode(self, ids: List[int]) -> str:
        out = []
        for i in ids:
            t = self.itos.get(int(i), "")
            if t in (self.PAD, self.BOS, self.EOS):
                continue
            out.append(t)
        return "".join(out)


@dataclass
class CurriculumStage:
    task: str            # "arith" | "compare" | "dots2num"
    max_n: int           # digits for arith; max dots for dot tasks
    p_add: float = 1.0
    p_sub: float = 0.0
    p_mul: float = 0.0
    p_div: float = 0.0   # exact division only


class MathSampleGenerator:
    def __init__(self, op_mode: str, seed: int = 0):
        self.op_mode = op_mode  # "add"|"sub"|"mul"|"div"|"mix"
        self.rng = random.Random(seed)

    def _rand_int_with_digits(self, digits: int) -> int:
        hi = 10**digits - 1
        return self.rng.randint(0, hi)

    def _dots(self, n: int) -> str:
        return "•" * n

    # baby tasks
    def _make_compare(self, max_n: int) -> Tuple[str, str]:
        a = self.rng.randint(0, max_n)
        b = self.rng.randint(0, max_n)
        q = f"{self._dots(a)}?{self._dots(b)}="
        if a > b:
            y = "L\n"
        elif a < b:
            y = "R\n"
        else:
            y = "=\n"
        return q, y

    def _make_dots2num(self, max_n: int) -> Tuple[str, str]:
        a = self.rng.randint(0, max_n)
        q = f"{self._dots(a)}->"  # '-' then '>' (char-level)
        y = f"{a}\n"
        return q, y

    # arithmetic tasks
    def _make_problem(self, op: str, max_digits: int) -> Tuple[str, str]:
        a = self._rand_int_with_digits(max_digits)
        b = self._rand_int_with_digits(max_digits)

        if op == "+":
            return f"{a}+{b}=", f"{a+b}\n"

        if op == "-":
            if b > a:
                a, b = b, a
            return f"{a}-{b}=", f"{a-b}\n"

        if op == "*":
            b_digits = max(1, max_digits - 1)
            a = self._rand_int_with_digits(max_digits)
            b = self._rand_int_with_digits(b_digits)
            return f"{a}*{b}=", f"{a*b}\n"

        if op == "/":
            b = max(1, self._rand_int_with_digits(max_digits))
            k_digits = max(1, max_digits - 1)
            k = self._rand_int_with_digits(k_digits)
            a = b * k
            return f"{a}/{b}=", f"{k}\n"

        raise ValueError(f"Unknown op: {op}")

    def _pick_op_mix(self, stage: CurriculumStage) -> str:
        r = self.rng.random()
        c_add = stage.p_add
        c_sub = c_add + stage.p_sub
        c_mul = c_sub + stage.p_mul
        c_div = c_mul + stage.p_div
        if r < c_add:
            return "+"
        elif r < c_sub:
            return "-"
        elif r < c_mul:
            return "*"
        else:
            return "/"

    def sample(self, stage: CurriculumStage) -> Tuple[str, str]:
        if stage.task == "compare":
            return self._make_compare(stage.max_n)
        if stage.task == "dots2num":
            return self._make_dots2num(stage.max_n)

        max_digits = stage.max_n
        if self.op_mode in ("add", "sub", "mul", "div"):
            op = {"add": "+", "sub": "-", "mul": "*", "div": "/"}[self.op_mode]
            return self._make_problem(op, max_digits)

        op = self._pick_op_mix(stage)
        return self._make_problem(op, max_digits)


class TinyTransformerLM(nn.Module):
    def __init__(self, vocab_size: int, d_model: int = 128, n_heads: int = 4, n_layers: int = 4,
                 dropout: float = 0.1, max_len: int = 128):
        super().__init__()
        self.max_len = max_len
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_len, d_model)

        enc_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_model * 4,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.enc = nn.TransformerEncoder(enc_layer, num_layers=n_layers)
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, x: torch.Tensor, attn_mask: torch.Tensor) -> torch.Tensor:
        B, T = x.shape
        if T > self.max_len:
            raise ValueError(f"Sequence length {T} > max_len {self.max_len}")
        pos = torch.arange(T, device=x.device).unsqueeze(0).expand(B, T)
        h = self.tok_emb(x) + self.pos_emb(pos)
        h = self.enc(h, mask=attn_mask)
        h = self.ln_f(h)
        return self.head(h)


def causal_mask(T: int, device: torch.device) -> torch.Tensor:
    m = torch.full((T, T), float("-inf"), device=device)
    return torch.triu(m, diagonal=1)


def make_batch(gen: MathSampleGenerator, tok: CharTokenizer, stage: CurriculumStage,
               batch_size: int, device: torch.device, max_len: int) -> Tuple[torch.Tensor, torch.Tensor]:
    xs: List[List[int]] = []
    loss_masks: List[List[int]] = []

    for _ in range(batch_size):
        q, y = gen.sample(stage)
        seq = tok.encode(q + y, add_bos_eos=True)
        if len(seq) > max_len:
            q, y = gen.sample(stage)
            seq = tok.encode(q + y, add_bos_eos=True)

        q_ids = tok.encode(q, add_bos_eos=False)
        y_ids = tok.encode(y, add_bos_eos=False)
        start_y = 1 + len(q_ids)
        end_y = start_y + len(y_ids)

        mask = [0] * len(seq)
        for i in range(start_y, min(end_y, len(seq))):
            mask[i] = 1
        mask[-1] = 1  # EOS

        xs.append(seq)
        loss_masks.append(mask)

    T = min(max(len(s) for s in xs), max_len)
    x_pad = torch.full((batch_size, T), tok.pad_id, dtype=torch.long)
    m_pad = torch.zeros((batch_size, T), dtype=torch.float32)
    for i, (s, m) in enumerate(zip(xs, loss_masks)):
        s = s[:T]
        m = m[:T]
        x_pad[i, :len(s)] = torch.tensor(s, dtype=torch.long)
        m_pad[i, :len(m)] = torch.tensor(m, dtype=torch.float32)

    return x_pad.to(device), m_pad.to(device)


@torch.no_grad()
def greedy_solve(model: TinyTransformerLM, tok: CharTokenizer, prompt: str,
                 device: torch.device, max_new_tokens: int = 96) -> str:
    model.eval()
    ids = tok.encode(prompt, add_bos_eos=False)
    x = torch.tensor([tok.bos_id] + ids, dtype=torch.long, device=device).unsqueeze(0)

    for _ in range(max_new_tokens):
        T = x.size(1)
        attn = causal_mask(T, device)
        logits = model(x, attn)[:, -1, :]
        nxt = torch.argmax(logits, dim=-1, keepdim=True)
        x = torch.cat([x, nxt], dim=1)
        if int(nxt.item()) == tok.eos_id:
            break

    out = tok.decode(x.squeeze(0).tolist())
    if "=" in out:
        return out.split("=", 1)[1]
    if "->" in out:
        return out.split("->", 1)[1]
    return out


def exact_match(pred: str, gold: str) -> bool:
    return pred.strip() == gold.strip()


def make_curriculum_mother(op_mode: str) -> List[CurriculumStage]:
    stages: List[CurriculumStage] = []
    for d in [1, 2, 3, 4]:
        if op_mode == "mix":
            if d == 1:
                stages.append(CurriculumStage(task="arith", max_n=1, p_add=1.0))
            elif d == 2:
                stages.append(CurriculumStage(task="arith", max_n=2, p_add=0.7, p_sub=0.3))
            elif d == 3:
                stages.append(CurriculumStage(task="arith", max_n=3, p_add=0.5, p_sub=0.3, p_mul=0.2))
            else:
                stages.append(CurriculumStage(task="arith", max_n=4, p_add=0.4, p_sub=0.25, p_mul=0.25, p_div=0.10))
        else:
            stages.append(CurriculumStage(task="arith", max_n=d))
    return stages


def make_curriculum_baby(op_mode: str) -> List[CurriculumStage]:
    baby: List[CurriculumStage] = [
        CurriculumStage(task="compare", max_n=3),
        CurriculumStage(task="compare", max_n=6),
        CurriculumStage(task="dots2num", max_n=6),
        CurriculumStage(task="dots2num", max_n=9),
    ]
    baby.extend(make_curriculum_mother(op_mode))
    return baby


def stage_for_step(stages: List[CurriculumStage], step: int, total_steps: int) -> CurriculumStage:
    k = len(stages)
    chunk = max(1, total_steps // k)
    idx = min(k - 1, step // chunk)
    return stages[idx]


@torch.no_grad()
def eval_task(model: TinyTransformerLM, tok: CharTokenizer, device: torch.device,
              op_mode: str, task: str, max_n: int, n: int = 200) -> float:
    gen = MathSampleGenerator(op_mode=op_mode, seed=1234 + max_n * 17 + len(task))
    stage = CurriculumStage(task=task, max_n=max_n)
    correct = 0
    for _ in range(n):
        q, y = gen.sample(stage)
        pred = greedy_solve(model, tok, q, device, max_new_tokens=96)
        if exact_match(pred, y):
            correct += 1
    return correct / n


@torch.no_grad()
def eval_arith_ood(model: TinyTransformerLM, tok: CharTokenizer, device: torch.device,
                   op_mode: str, train_digits: int, test_digits: int, n: int = 200) -> float:
    gen = MathSampleGenerator(op_mode=op_mode, seed=54321 + test_digits)
    stage = CurriculumStage(task="arith", max_n=test_digits)
    correct = 0
    for _ in range(n):
        q, y = gen.sample(stage)
        pred = greedy_solve(model, tok, q, device, max_new_tokens=128)
        if exact_match(pred, y):
            correct += 1
    return correct / n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", type=str, default="baby", choices=["baby", "mother"])
    ap.add_argument("--op", type=str, default="add", choices=["add", "sub", "mul", "div", "mix"])
    ap.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--train_steps", type=int, default=40000)
    ap.add_argument("--batch_size", type=int, default=128)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--d_model", type=int, default=128)
    ap.add_argument("--n_layers", type=int, default=4)
    ap.add_argument("--n_heads", type=int, default=4)
    ap.add_argument("--dropout", type=float, default=0.1)
    ap.add_argument("--max_len", type=int, default=80)
    ap.add_argument("--eval_every", type=int, default=2000)
    ap.add_argument("--save_path", type=str, default="mama_baby_math.pt")
    args = ap.parse_args()

    set_seed(args.seed)
    device = torch.device(args.device)

    tok = CharTokenizer()
    model = TinyTransformerLM(
        vocab_size=len(tok.tokens),
        d_model=args.d_model,
        n_heads=args.n_heads,
        n_layers=args.n_layers,
        dropout=args.dropout,
        max_len=args.max_len
    ).to(device)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = MathSampleGenerator(op_mode=args.op, seed=args.seed)

    curriculum = make_curriculum_baby(args.op) if args.mode == "baby" else make_curriculum_mother(args.op)

    print(f"[info] mode={args.mode} op={args.op} device={device} vocab={len(tok.tokens)}")
    print(f"[info] steps={args.train_steps} batch={args.batch_size} lr={args.lr}")
    print(f"[info] curriculum_len={len(curriculum)} stages={curriculum}")

    for step in range(args.train_steps):
        model.train()
        stage = stage_for_step(curriculum, step, args.train_steps)

        x, loss_mask = make_batch(gen, tok, stage, args.batch_size, device, args.max_len)
        T = x.size(1)
        attn = causal_mask(T, device)
        logits = model(x, attn)

        targets = x[:, 1:].contiguous()
        logits = logits[:, :-1, :].contiguous()
        mask = loss_mask[:, 1:]

        loss_per_tok = F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                       targets.reshape(-1),
                                       reduction="none").view(targets.size(0), targets.size(1))
        loss = (loss_per_tok * mask).sum() / (mask.sum() + 1e-8)

        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if (step + 1) % 200 == 0:
            print(f"step {step+1:6d} | task={stage.task:7s} | max_n={stage.max_n:2d} | loss {loss.item():.4f}")

        if (step + 1) % args.eval_every == 0:
            print(f"[eval@{step+1}] current_stage: task={stage.task} max_n={stage.max_n}")

            if args.mode == "baby":
                for mx in [3, 6, 9]:
                    acc = eval_task(model, tok, device, args.op, "compare", mx, n=300)
                    print(f"  [compare]  max_n={mx:2d} acc={acc:.3f}")
                for mx in [6, 9, 12]:
                    acc = eval_task(model, tok, device, args.op, "dots2num", mx, n=300)
                    print(f"  [dots2num] max_n={mx:2d} acc={acc:.3f}")

            train_d = stage.max_n if stage.task == "arith" else 1
            for test_d in [train_d, train_d + 1, train_d + 2]:
                acc = eval_arith_ood(model, tok, device, args.op, train_d, test_d, n=200)
                print(f"  [arith] train_digits={train_d} test_digits={test_d} acc={acc:.3f}")

            # qualitative samples
            for _ in range(3):
                q, y = gen.sample(stage)
                pred = greedy_solve(model, tok, q, device, max_new_tokens=128)
                print(f"    Q: {q}  pred: {pred.strip()}  gold: {y.strip()}")

    ckpt = {"model": model.state_dict(), "args": vars(args), "tokens": tok.tokens}
    torch.save(ckpt, args.save_path)
    print(f"[done] saved {args.save_path}")


if __name__ == "__main__":
    main()
