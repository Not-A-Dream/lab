"""
Aurora README.md → 한국어 번역 PDF 생성
출력: my-folder/L/aurora_ko.pdf
연구 및 학습 목적 전용
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    HRFlowable, PageBreak, Preformatted, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 한국어 폰트 등록 ─────────────────────────────────────────
FONT_DIR = "C:/Windows/Fonts"
pdfmetrics.registerFont(TTFont("Malgun",   os.path.join(FONT_DIR, "malgun.ttf")))
pdfmetrics.registerFont(TTFont("MalgunBd", os.path.join(FONT_DIR, "malgunbd.ttf")))

# ── 경로 설정 ─────────────────────────────────────────────────
DOC_DIR = "C:/Discovery/Cosmo/dev/lab/time-series/aurora/doc"
OUTPUT  = "C:/Discovery/Cosmo/dev/lab/my-folder/L/aurora_ko.pdf"

# ── 스타일 ───────────────────────────────────────────────────
def style(name, **kw):
    base = ParagraphStyle(name, fontName="Malgun", fontSize=9, leading=15)
    for k, v in kw.items():
        setattr(base, k, v)
    return base

S = {
    "cover_title": style("cover_title", fontName="MalgunBd", fontSize=32,
                         leading=40, alignment=TA_CENTER,
                         textColor=colors.HexColor("#1a1a2e")),
    "cover_sub":   style("cover_sub", fontSize=12, leading=18,
                         alignment=TA_CENTER, textColor=colors.HexColor("#444444")),
    "cover_conf":  style("cover_conf", fontSize=10, alignment=TA_CENTER,
                         textColor=colors.HexColor("#e94560")),
    "disclaimer":  style("disclaimer", fontSize=8, leading=13,
                         alignment=TA_CENTER, textColor=colors.HexColor("#888888")),
    "section":     style("section", fontName="MalgunBd", fontSize=16, leading=22,
                         spaceAfter=8, textColor=colors.white,
                         backColor=colors.HexColor("#1a1a2e"),
                         borderPadding=(5, 8, 5, 8)),
    "h2":          style("h2", fontName="MalgunBd", fontSize=13, leading=18,
                         spaceBefore=8, spaceAfter=4,
                         textColor=colors.HexColor("#16213e")),
    "h3":          style("h3", fontName="MalgunBd", fontSize=11, leading=15,
                         spaceBefore=5, spaceAfter=3,
                         textColor=colors.HexColor("#0f3460")),
    "body":        style("body", fontSize=9, leading=15, spaceAfter=4,
                         alignment=TA_JUSTIFY),
    "bullet":      style("bullet", fontSize=9, leading=15, leftIndent=12),
    "code":        style("code", fontName="Courier", fontSize=7.5, leading=11,
                         backColor=colors.HexColor("#f4f4f4"),
                         leftIndent=8, rightIndent=8,
                         spaceBefore=4, spaceAfter=4),
    "caption":     style("caption", fontSize=8, leading=12,
                         alignment=TA_CENTER, textColor=colors.HexColor("#666666")),
    "label":       style("label", fontName="MalgunBd", fontSize=8,
                         textColor=colors.HexColor("#e94560")),
}

# ── 이미지 헬퍼 ──────────────────────────────────────────────
def img(filename, width_mm=130):
    path = os.path.join(DOC_DIR, filename)
    if not os.path.exists(path):
        return None
    i = Image(path)
    ratio = i.imageHeight / i.imageWidth
    w = width_mm * mm
    return Image(path, width=w, height=w * ratio)

# ── 번역 콘텐츠 ──────────────────────────────────────────────
def build_story():
    story = []

    # ── 표지 ──────────────────────────────────────────────────
    story.append(Spacer(1, 35*mm))
    logo = img("logo.png", 28)
    if logo:
        story.append(logo)
        story.append(Spacer(1, 6*mm))
    story.append(Paragraph("Aurora", S["cover_title"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "범용 생성형 멀티모달 시계열 예측을 향하여", S["cover_sub"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Towards Universal Generative Multimodal Time Series Forecasting",
        style("cover_en", fontSize=9, alignment=TA_CENTER,
              textColor=colors.HexColor("#888888"))))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("ICLR 2026", S["cover_conf"]))
    story.append(Spacer(1, 12*mm))
    story.append(HRFlowable(width="60%", thickness=0.5,
                             color=colors.HexColor("#cccccc"), hAlign="CENTER"))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "본 문서는 순수한 연구 및 학습 목적으로만 작성되었습니다.<br/>"
        "상업적 목적의 사용·배포·재가공을 금하며, 원 저작권은 논문 저자에게 있습니다.<br/>"
        "For research and educational purposes only. Not for commercial use.",
        S["disclaimer"]))
    story.append(PageBreak())

    # ── 1. 소개 ───────────────────────────────────────────────
    story.append(Paragraph("1. 소개 (Introduction)", S["section"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Aurora는 고성능 멀티모달 시계열 파운데이션 모델입니다. "
        "<b>모달리티 가이드 멀티헤드 자기 어텐션(Modality-Guided Multi-head Self-Attention)</b>과 "
        "<b>프로토타입 가이드 플로우 매칭(Prototype-Guided Flow Matching)</b>을 기반으로, "
        "도메인 특화 지식을 효과적으로 활용하며 생성형 확률적 예측을 지원합니다. "
        "다양한 예측 시나리오를 포괄하는 최초의 사전 학습된 멀티모달 시계열 파운데이션 모델로, "
        "TimeMMD·TSFM-Bench·ProbTS·TFB·EPF 등 5개 벤치마크에서 최고 수준의 성능을 기록하였습니다.",
        S["body"]))
    story.append(Spacer(1, 3*mm))
    intro = img("intro.png", 120)
    if intro:
        story.append(intro)
        story.append(Paragraph("Figure 1 — Aurora 개요", S["caption"]))
    story.append(Spacer(1, 4*mm))

    # ── 2. 아키텍처 ────────────────────────────────────────────
    story.append(Paragraph("2. 아키텍처 (Architecture)", S["section"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Aurora는 <b>크로스 모달리티 패러다임</b>으로 사전 학습됩니다. "
        "시계열 데이터에 채널 독립성(Channel Independence)을 적용하고, "
        "각 변수는 인스턴스 정규화(Instance Normalization)를 통해 값 차이를 완화한 후 독립 처리됩니다. "
        "대응하는 멀티모달 상호작용을 모델링하여 도메인 지식을 주입합니다.",
        S["body"]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("인코더 (Aurora Encoder)", S["h2"]))
    for t in [
        "각 모달리티 데이터를 토큰화하고 독립적으로 인코딩하여 모달 피처(modal features)를 생성합니다.",
        "생성된 모달 피처들을 크로스 어텐션/크로스 모달 게이트를 통해 융합하여 "
        "다중 모달 표현(multimodal representations)을 생성합니다.",
        "단순 연결(concatenation)이 아닌, 상호작용을 통한 새로운 표현 공간 생성이 핵심입니다.",
    ]:
        story.append(Paragraph(f"• {t}", S["bullet"]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("디코더 (Aurora Decoder)", S["h2"]))
    for t in [
        "조건부 디코더(Condition Decoder): 미래 토큰의 멀티모달 조건을 추정합니다.",
        "프로토타입 리트리버(Prototype Retriever): 도메인 지식 기반으로 미래 프로토타입을 검색합니다. "
        "이는 시계열 분야의 RAG(검색 증강 생성)로 볼 수 있습니다.",
        "플로우 매칭(Flow Matching): 프로토타입 분포 비교를 통해 확률적 예측을 생성합니다.",
    ]:
        story.append(Paragraph(f"• {t}", S["bullet"]))
    story.append(Spacer(1, 3*mm))
    arch = img("arch.png", 135)
    if arch:
        story.append(arch)
        story.append(Paragraph("Figure 2 — Aurora 아키텍처 전체 구조", S["caption"]))
    story.append(PageBreak())

    # ── 3. 핵심 개념 ──────────────────────────────────────────
    story.append(Paragraph("3. 핵심 개념 정리", S["section"]))
    story.append(Spacer(1, 3*mm))

    concepts = [
        ("채널 독립성\n(Channel Independence)",
         "각 시계열 변수(온도·습도·전력 등)를 독립적으로 처리.\n"
         "인스턴스 정규화로 스케일 차이 보정."),
        ("멀티모달 융합\n(Multimodal Fusion)",
         "독립 인코딩 결과를 Attention/Cross-modal Gate로 상호작용.\n"
         "단순 Concatenation이 아닌 새로운 표현 공간 생성."),
        ("프로토타입 리트리버\n(Prototype Retriever)",
         "데이터베이스에서 유사 과거 패턴 검색.\n"
         "도메인 지식을 예측에 직접 반영 (시계열판 RAG)."),
        ("플로우 매칭\n(Flow Matching)",
         "미래 값의 확률 분포를 계산하는 적응형 변환.\n"
         "단일 값이 아닌 분포 기반 불확실성 표현."),
        ("인스턴스 정규화\n(Instance Normalization)",
         "각 변수별 평균·표준편차로 스케일 차이 보정.\n"
         "서로 다른 물리적 단위 간 비교 가능하게 함."),
    ]
    tdata = [["개념", "설명"]]
    for c, d in concepts:
        tdata.append([
            Paragraph(c, S["label"]),
            Paragraph(d.replace("\n", "<br/>"), S["body"])
        ])
    t = Table(tdata, colWidths=[42*mm, 120*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",   (0,0), (-1,0),  colors.white),
        ("FONTNAME",    (0,0), (-1,0),  "MalgunBd"),
        ("FONTSIZE",    (0,0), (-1,0),  9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#f8f8f8"), colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ── 4. 빠른 시작 ──────────────────────────────────────────
    story.append(Paragraph("4. 빠른 시작 (Quickstart)", S["section"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("설치", S["h2"]))
    story.append(Preformatted("pip install aurora-model==0.1.0", S["code"]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("단일 모달 시계열 예측 (Unimodal)", S["h2"]))
    story.append(Paragraph(
        "단일 시계열 변수만 입력으로 사용하는 기본 예측 방식입니다.",
        S["body"]))
    story.append(Preformatted(
"""from aurora import load_model
import torch

model = load_model()

# 입력 데이터 준비
batch_size, lookback_length = 1, 528   # 배치 크기, 과거 참조 길이
seqs = torch.randn(batch_size, lookback_length).cuda()

# 예측 파라미터
forecast_length = 96   # 예측 길이
num_samples     = 100  # 샘플 수 (불확실성 표현)

# inference_token_len: 데이터 주기 길이 권장 (예: 48시간 주기)
output = model.generate(
    inputs=seqs,
    max_output_length=forecast_length,
    num_samples=num_samples,
    inference_token_len=48
)
# output.shape: [batch, samples, forecast_length, modality]
print(output.shape)""", S["code"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("멀티모달 시계열 예측 (Multimodal)", S["h2"]))
    story.append(Paragraph(
        "시계열 데이터와 텍스트 정보(날짜·도메인 설명 등)를 함께 입력하여 "
        "도메인 지식을 예측에 반영하는 방식입니다.",
        S["body"]))
    story.append(Preformatted(
"""from aurora import load_model
from einops import rearrange
import torch

model     = load_model()
tokenizer = model.tokenizer

# 입력 설정
batch_size, n_vars = 1, 10
lookback_length    = 528
seqs = torch.randn(batch_size, lookback_length, n_vars).cuda()

# 텍스트 입력 (날짜·도메인 정보)
text = "1983-09-12: Federal Register legal notices..."
tokenized = tokenizer(text, padding='max_length',
                      truncation=True, max_length=200,
                      return_tensors="pt")

text_ids   = tokenized['input_ids'].repeat(n_vars, 1).cuda()
text_mask  = tokenized['attention_mask'].repeat(n_vars, 1).cuda()
text_types = tokenized.get('token_type_ids',
             torch.zeros_like(text_ids)).cuda()
batch_x    = rearrange(seqs, "b l c -> (b c) l")

output = model.generate(
    inputs=batch_x,
    text_input_ids=text_ids,
    text_attention_mask=text_mask,
    text_token_type_ids=text_types,
    max_output_length=96,
    num_samples=100,
    inference_token_len=48
)
print(output.shape)""", S["code"]))
    story.append(PageBreak())

    # ── 5. 실험 성능 ──────────────────────────────────────────
    story.append(Paragraph("5. 실험 성능 (Performance)", S["section"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Aurora는 5개 벤치마크(TimeMMD·TSFM-Bench·ProbTS·TFB·EPF) 전반에 걸쳐 "
        "일관된 최고 수준의 성능을 달성하였습니다.",
        S["body"]))
    story.append(Spacer(1, 3*mm))
    for i, (fname, cap) in enumerate([
        ("table1.png", "Table 1 — TimeMMD 벤치마크 결과"),
        ("table2.png", "Table 2 — TSFM-Bench 결과"),
        ("table3.png", "Table 3 — ProbTS 결과"),
        ("table4.png", "Table 4 — TFB 결과"),
        ("table5.png", "Table 5 — EPF 결과"),
    ]):
        image = img(fname, 145)
        if image:
            story.append(image)
            story.append(Paragraph(cap, S["caption"]))
            story.append(Spacer(1, 4*mm))
    story.append(PageBreak())

    # ── 6. 인용 ────────────────────────────────────────────────
    story.append(Paragraph("6. 인용 (Citation)", S["section"]))
    story.append(Spacer(1, 3*mm))
    story.append(Preformatted(
"""@inproceedings{wu2026aurora,
  title     = {Aurora: Towards Universal Generative
               Multimodal Time Series Forecasting},
  author    = {Wu, Xingjian and Jin, Jianxin and Qiu, Wanghui
               and Chen, Peng and Shu, Yang
               and Yang, Bin and Guo, Chenjuan},
  booktitle = {ICLR},
  year      = {2026}
}""", S["code"]))
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width="100%", thickness=0.3,
                             color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "본 문서는 순수한 연구 및 학습 목적으로만 작성되었습니다. "
        "상업적 목적의 사용·배포·재가공을 금하며, 원 저작권은 논문 저자에게 있습니다.<br/>"
        "For research and educational purposes only. Not for commercial use.",
        S["disclaimer"]))

    return story


# ── PDF 빌드 ─────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm,  bottomMargin=18*mm,
    )
    doc.build(build_story())
    print(f"PDF 생성 완료: {OUTPUT}")

if __name__ == "__main__":
    build_pdf()
