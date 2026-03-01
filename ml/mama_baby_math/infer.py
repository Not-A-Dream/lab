#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
infer.py

Load a trained checkpoint from mama_baby_math.py and run interactive inference.

Examples:
  python infer.py --ckpt mama_baby_math.pt --device cpu
  python infer.py --ckpt mama_baby_math.pt --device cuda

Then type prompts like:
  •••?••=
  •••••->      (dots-to-number)
  12+34=
  99+7=
Type :quit to exit.
"""

import argparse
from typing import List

import torch
import torch.nn as nn


# --------- Minimal model definitions (must match training) ---------
class TinyTransformerLM(nn.Module):
    def __init__(self, vocab_size: int, d_model: int, n_heads: int, n_layers: int, dropout: float, max_len: int):
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


class CharTokenizer:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.stoi = {t: i for i, t in enumerate(tokens)}
        self.itos = {i: t for t, i in self.stoi.items()}
        self.PAD = "<pad>"
        self.BOS = "<bos>"
        self.EOS = "<eos>"

    @property
    def pad_id(self): return self.stoi[self.PAD]
    @property
    def bos_id(self): return self.stoi[self.BOS]
    @property
    def eos_id(self): return self.stoi[self.EOS]

    def encode(self, s: str, add_bos: bool = True) -> List[int]:
        ids = []
        for ch in s:
            if ch not in self.stoi:
                raise ValueError(f"Unknown char: {repr(ch)}. Allowed: {self.tokens}")
            ids.append(self.stoi[ch])
        return ([self.bos_id] + ids) if add_bos else ids

    def decode(self, ids: List[int]) -> str:
        out = []
        for i in ids:
            t = self.itos.get(int(i), "")
            if t in (self.PAD, self.BOS, self.EOS):
                continue
            out.append(t)
        return "".join(out)


@torch.no_grad()
def greedy_generate(model: TinyTransformerLM, tok: CharTokenizer, prompt: str, device: torch.device, max_new_tokens: int = 96) -> str:
    model.eval()
    x = torch.tensor(tok.encode(prompt, add_bos=True), dtype=torch.long, device=device).unsqueeze(0)

    for _ in range(max_new_tokens):
        T = x.size(1)
        attn = causal_mask(T, device)
        logits = model(x, attn)[:, -1, :]
        nxt = torch.argmax(logits, dim=-1, keepdim=True)
        x = torch.cat([x, nxt], dim=1)
        if int(nxt.item()) == tok.eos_id:
            break

    out = tok.decode(x.squeeze(0).tolist())
    # return generated part after '=' or '->' if present
    if "=" in out:
        return out.split("=", 1)[1]
    if "->" in out:
        return out.split("->", 1)[1]
    return out


def pick_device(requested: str) -> torch.device:
    if requested == "cuda":
        if torch.cuda.is_available():
            return torch.device("cuda")
        print("[warn] CUDA requested but not available. Falling back to CPU.")
        return torch.device("cpu")
    return torch.device("cpu")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", type=str, default="mama_baby_math.pt", help="checkpoint path saved by mama_baby_math.py")
    ap.add_argument("--device", type=str, default="cpu", choices=["cpu", "cuda"])
    ap.add_argument("--max_new_tokens", type=int, default=96)
    args = ap.parse_args()

    device = pick_device(args.device)

    ckpt = torch.load(args.ckpt, map_location=device)
    tokens = ckpt["tokens"]
    train_args = ckpt.get("args", {})

    tok = CharTokenizer(tokens=tokens)

    # Pull architecture from saved args (fallback to reasonable defaults)
    d_model = int(train_args.get("d_model", 128))
    n_layers = int(train_args.get("n_layers", 4))
    n_heads = int(train_args.get("n_heads", 4))
    dropout = float(train_args.get("dropout", 0.1))
    max_len = int(train_args.get("max_len", 80))

    model = TinyTransformerLM(
        vocab_size=len(tokens),
        d_model=d_model,
        n_heads=n_heads,
        n_layers=n_layers,
        dropout=dropout,
        max_len=max_len,
    ).to(device)
    model.load_state_dict(ckpt["model"], strict=True)
    model.eval()

    print(f"[info] loaded {args.ckpt}")
    print(f"[info] device={device} vocab={len(tokens)} d_model={d_model} layers={n_layers} heads={n_heads} max_len={max_len}")
    print("입력을 넣고 Enter를 누르세요. 종료: :quit / :q")
    print("예시: 12+34=   |  •••?••=   |  •••••->")

    while True:
        try:
            prompt = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[bye]")
            break

        if prompt in (":quit", ":q", "quit", "exit"):
            print("[bye]")
            break
        if not prompt:
            continue

        try:
            ans = greedy_generate(model, tok, prompt, device, max_new_tokens=args.max_new_tokens)
            print(ans.strip())
        except Exception as e:
            print(f"[error] {e}")


if __name__ == "__main__":
    main()
