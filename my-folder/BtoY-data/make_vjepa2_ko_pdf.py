"""
V-JEPA 2 README.md → 한국어 번역 PDF 생성
출력: my-folder/BtoY-data/vjepa2_ko.pdf
연구 및 학습 목적 전용
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
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
OUTPUT = "C:/Discovery/Cosmo/dev/lab/my-folder/BtoY-data/vjepa2_ko.pdf"

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
    "new_badge":   style("new_badge", fontName="MalgunBd", fontSize=9,
                         textColor=colors.HexColor("#e94560")),
}


# ── 번역 콘텐츠 ──────────────────────────────────────────────
def build_story():
    story = []

    # ── 표지 ──────────────────────────────────────────────────
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("V-JEPA 2", S["cover_title"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "자기지도 비디오 모델을 통한 이해·예측·계획", S["cover_sub"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Self-Supervised Video Models Enable Understanding, Prediction and Planning",
        style("cover_en", fontSize=9, alignment=TA_CENTER,
              textColor=colors.HexColor("#888888"))))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Meta FAIR · 2025 (V-JEPA 2.1: 2026-03-16)", S["cover_conf"]))
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
        "V-JEPA 2는 Meta FAIR이 2025년 발표한 자기지도 비디오 인코더 학습 방법론입니다. "
        "인터넷 규모의 자연 비디오 데이터를 활용하여 <b>마스킹된 잠재 피처 예측</b> 목적함수로 사전학습되며, "
        "<b>동작 이해(motion understanding)</b>와 <b>인간 행동 예측(action anticipation)</b> 태스크에서 "
        "최고 수준의 성능을 달성합니다.",
        S["body"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "V-JEPA 2-AC는 V-JEPA 2를 기반으로 소량의 로봇 궤적 데이터로 후학습(post-training)한 "
        "<b>잠재 행동 조건부 세계 모델(latent action-conditioned world model)</b>로, "
        "환경별 데이터 수집·태스크별 학습·캘리브레이션 없이 로봇 조작 태스크를 수행합니다.",
        S["body"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "[NEW] V-JEPA 2.1 (2026-03-16)",
        S["new_badge"]))
    story.append(Paragraph(
        "V-JEPA 2.1은 고품질·시간적 일관성 있는 밀집 피처(dense features) 학습에 집중한 "
        "개선된 학습 레시피를 적용한 모델 패밀리입니다.",
        S["body"]))
    story.append(PageBreak())

    # ── 2. 방법론 ──────────────────────────────────────────────
    story.append(Paragraph("2. 방법론 (Method)", S["section"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("V-JEPA 2 사전학습", S["h2"]))
    story.append(Paragraph(
        "인코더와 예측기를 비디오 데이터로 자기지도 방식으로 공동 사전학습합니다. "
        "마스킹된 영역의 잠재 피처를 예측하는 방식으로, "
        "물리적 세계 이해와 예측 능력을 자연스럽게 부트스트랩합니다.",
        S["body"]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("V-JEPA 2-AC 후학습", S["h2"]))
    story.append(Paragraph(
        "소량의 로봇 데이터로 V-JEPA 2를 이미지 목표 기반 계획(image-goal planning)이 가능한 "
        "행동 조건부 세계 모델로 후학습합니다. "
        "Franka 로봇 팔에 단안 RGB 카메라만을 사용하여 도달·파지·픽앤플레이스 태스크를 수행합니다.",
        S["body"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("V-JEPA 2.1 핵심 기법", S["h2"]))
    techniques = [
        ("밀집 예측 손실\n(Dense Predictive Loss)",
         "마스킹 기반 자기지도 목적함수로, "
         "가시 토큰과 마스킹 토큰 모두 학습 손실에 기여.\n"
         "기존 방식 대비 더 풍부한 밀집 피처 학습."),
        ("심층 자기지도\n(Deep Self-Supervision)",
         "인코더의 여러 중간 표현에 자기지도 손실을 적용.\n"
         "계층적 표현 품질 향상."),
        ("멀티모달 토크나이저\n(Multi-Modal Tokenizers)",
         "이미지와 비디오를 위한 멀티모달 토크나이저 활용.\n"
         "다양한 입력 해상도 및 형식 지원."),
        ("모델·데이터 스케일링\n(Model & Data Scaling)",
         "ViT-B(80M)부터 ViT-G(2B)까지 스케일 확장 실험.\n"
         "스케일 증가에 따른 성능 향상 확인."),
    ]
    tdata = [["기법", "설명"]]
    for c, d in techniques:
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

    # ── 3. 핵심 개념 ──────────────────────────────────────────
    story.append(Paragraph("3. 핵심 개념 정리", S["section"]))
    story.append(Spacer(1, 3*mm))

    concepts = [
        ("세계 모델\n(World Model)",
         "환경의 물리적 동작을 내부적으로 시뮬레이션하는 모델.\n"
         "V-JEPA 2는 비디오에서 자기지도 방식으로 세계 모델을 학습."),
        ("행동 조건부 모델\n(Action-Conditioned\nModel)",
         "특정 행동이 주어졌을 때 미래 상태를 잠재 공간에서 예측.\n"
         "로봇 제어에서 명시적 환경 시뮬레이터 없이 계획 가능."),
        ("이미지 목표 계획\n(Image-Goal Planning)",
         "목표 상태를 이미지로 지정하면, 모델이 그 목표에 도달하기 위한\n"
         "행동 시퀀스를 잠재 공간에서 탐색."),
        ("밀집 피처\n(Dense Features)",
         "이미지/영상의 각 위치(토큰)마다 독립적인 피처 벡터를 추출.\n"
         "전역 평균이 아닌 공간적 세부 표현 — 세그멘테이션·깊이 추정에 유리."),
        ("마스킹 잠재 예측\n(Masked Latent\nPrediction)",
         "비디오 토큰 일부를 마스킹하고, 나머지 토큰으로 마스킹된 부분의\n"
         "잠재 표현을 예측. 픽셀 재구성 없이 의미론적 학습."),
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

    # ── 4. 사전학습 모델 ──────────────────────────────────────
    story.append(Paragraph("4. 사전학습 모델 (Pretrained Models)", S["section"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("V-JEPA 2 체크포인트", S["h2"]))
    v2_data = [["모델", "파라미터 수", "해상도"]]
    v2_models = [
        ("ViT-L/16", "300M", "256"),
        ("ViT-H/16", "600M", "256"),
        ("ViT-g/16", "1B",   "256"),
        ("ViT-g/16₃₈₄", "1B", "384"),
    ]
    for row in v2_models:
        v2_data.append([Paragraph(c, S["body"]) for c in row])

    t2 = Table(v2_data, colWidths=[50*mm, 40*mm, 40*mm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",   (0,0), (-1,0),  colors.white),
        ("FONTNAME",    (0,0), (-1,0),  "MalgunBd"),
        ("FONTSIZE",    (0,0), (-1,0),  9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#f8f8f8"), colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ]))
    story.append(t2)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("V-JEPA 2.1 체크포인트 (신규)", S["h2"]))
    v21_data = [["모델", "파라미터 수", "해상도"]]
    v21_models = [
        ("ViT-B/16", "80M",  "384"),
        ("ViT-L/16", "300M", "384"),
        ("ViT-g/16", "1B",   "384"),
        ("ViT-G/16", "2B",   "384"),
    ]
    for row in v21_models:
        v21_data.append([Paragraph(c, S["body"]) for c in row])

    t21 = Table(v21_data, colWidths=[50*mm, 40*mm, 40*mm])
    t21.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",   (0,0), (-1,0),  colors.white),
        ("FONTNAME",    (0,0), (-1,0),  "MalgunBd"),
        ("FONTSIZE",    (0,0), (-1,0),  9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#f8f8f8"), colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ]))
    story.append(t21)
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "모든 체크포인트는 HuggingFace collections(facebook/v-jepa-2) 및 "
        "facebookresearch/vjepa2 GitHub 저장소를 통해 제공됩니다.",
        S["body"]))
    story.append(PageBreak())

    # ── 5. 성능 ────────────────────────────────────────────────
    story.append(Paragraph("5. 성능 (Performance)", S["section"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("V-JEPA 2 벤치마크 결과", S["h2"]))
    bench_data = [["벤치마크", "V-JEPA 2", "이전 최고 성능"]]
    benchmarks = [
        ("EK100 (행동 예측)",       "39.7%", "27.6% (PlausiVL)"),
        ("SSv2 Probe (동작 이해)",  "77.3%", "69.7% (InternVideo2-1B)"),
        ("Diving48 Probe",          "90.2%", "86.4% (InternVideo2-1B)"),
        ("MVP Video QA",            "44.5%", "39.9% (InternVL-2.5)"),
        ("TempCompass Video QA",    "76.9%", "75.3% (Tarsier 2)"),
    ]
    for row in benchmarks:
        bench_data.append([Paragraph(c, S["body"]) for c in row])

    bt = Table(bench_data, colWidths=[60*mm, 30*mm, 72*mm])
    bt.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",   (0,0), (-1,0),  colors.white),
        ("FONTNAME",    (0,0), (-1,0),  "MalgunBd"),
        ("FONTSIZE",    (0,0), (-1,0),  9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#f8f8f8"), colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
        ("ALIGN",       (1,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(bt)
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph("V-JEPA 2-AC 로봇 조작 성능 (Franka 로봇 팔)", S["h2"]))
    robot_data = [["방법", "도달(Reach)", "파지-컵(Cup)", "파지-박스(Box)",
                   "픽앤플레이스-컵", "픽앤플레이스-박스"]]
    robots = [
        ("Octo",        "100%", "10%", "0%",  "10%", "10%"),
        ("Cosmos",      "80%",  "0%",  "20%", "0%",  "0%"),
        ("V-JEPA 2-AC", "100%", "60%", "20%", "80%", "50%"),
    ]
    for row in robots:
        robot_data.append([Paragraph(c, S["body"]) for c in row])

    rt = Table(robot_data, colWidths=[28*mm, 20*mm, 22*mm, 22*mm, 25*mm, 25*mm])
    rt.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",   (0,0), (-1,0),  colors.white),
        ("FONTNAME",    (0,0), (-1,0),  "MalgunBd"),
        ("FONTSIZE",    (0,0), (-1,0),  8),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.HexColor("#f8f8f8"), colors.white]),
        ("GRID",        (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
        ("ALIGN",       (1,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",  (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("FONTSIZE",    (0,1), (-1,-1), 8),
    ]))
    story.append(rt)
    story.append(PageBreak())

    # ── 6. 인용 ────────────────────────────────────────────────
    story.append(Paragraph("6. 인용 (Citation)", S["section"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("V-JEPA 2", S["h2"]))
    story.append(Preformatted(
"""@article{assran2025vjepa2,
  title   = {V-JEPA 2: Self-Supervised Video Models Enable
             Understanding, Prediction and Planning},
  author  = {Assran, Mahmoud and Bardes, Adrien and Fan, David
             and Garrido, Quentin and Howes, Russell
             and Komeili, Mojtaba and Muckley, Matthew
             and Rizvi, Ammar and Roberts, Claire
             and Sinha, Koustuv and {et al.}},
  journal = {arXiv preprint arXiv:2506.09985},
  year    = {2025}
}""", S["code"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("V-JEPA 2.1", S["h2"]))
    story.append(Preformatted(
"""@article{murlabadia2026vjepa21,
  title   = {V-JEPA 2.1 Pre-training},
  author  = {Mur-Labadia, Lorenzo and Muckley, Matthew and Bar, Amir
             and Assran, Mahmoud and Sinha, Koustuv
             and Rabbat, Michael and LeCun, Yann
             and Ballas, Nicolas and Bardes, Adrien},
  year    = {2026}
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
