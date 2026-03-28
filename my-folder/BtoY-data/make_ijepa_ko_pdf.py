"""
I-JEPA README.md → 한국어 번역 PDF 생성
출력: my-folder/BtoY-data/ijepa_ko.pdf
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
OUTPUT = "C:/Discovery/Cosmo/dev/lab/my-folder/BtoY-data/ijepa_ko.pdf"

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


# ── 번역 콘텐츠 ──────────────────────────────────────────────
def build_story():
    story = []

    # ── 표지 ──────────────────────────────────────────────────
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("I-JEPA", S["cover_title"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "이미지 기반 결합 임베딩 예측 아키텍처", S["cover_sub"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Image-based Joint-Embedding Predictive Architecture",
        style("cover_en", fontSize=9, alignment=TA_CENTER,
              textColor=colors.HexColor("#888888"))))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("CVPR 2023 · Meta AI Research (FAIR)", S["cover_conf"]))
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
        "I-JEPA는 Meta AI가 CVPR 2023에 발표한 자기지도학습(Self-Supervised Learning) 방법론입니다. "
        "핵심 아이디어는 <b>같은 이미지의 일부 표현(representation)으로 다른 부분의 표현을 예측</b>하는 것으로, "
        "픽셀 수준의 재구성이 아닌 <b>잠재 공간(latent space)에서의 예측</b>을 수행합니다. "
        "Yann LeCun이 제안한 JEPA(Joint-Embedding Predictive Architecture) 프레임워크를 이미지에 적용한 첫 번째 공식 구현입니다.",
        S["body"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("I-JEPA의 두 가지 핵심 차별점", S["h2"]))
    for t in [
        "<b>데이터 증강 불필요:</b> 손수 설계된 데이터 변환(회전·크롭·색상 변환 등)에 의존하지 않아 "
        "특정 다운스트림 태스크에 편향되지 않은 표현을 학습합니다.",
        "<b>픽셀 재구성 없음:</b> 픽셀 수준의 세부 정보를 복원하지 않으므로, "
        "더 의미론적으로 풍부한(semantically meaningful) 표현을 학습합니다.",
    ]:
        story.append(Paragraph(f"• {t}", S["bullet"]))
    story.append(Spacer(1, 4*mm))

    # ── 2. 방법론 ──────────────────────────────────────────────
    story.append(Paragraph("2. 방법론 (Method)", S["section"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "I-JEPA는 세 가지 네트워크 컴포넌트로 구성됩니다: "
        "<b>컨텍스트 인코더(Context Encoder)</b>, <b>타깃 인코더(Target Encoder)</b>, "
        "<b>예측기(Predictor)</b>.",
        S["body"]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("학습 절차", S["h2"]))
    steps = [
        ("1단계 — 마스킹",
         "입력 이미지를 여러 블록으로 분할합니다. "
         "일부 블록은 컨텍스트(context)로, 나머지 블록은 타깃(target)으로 지정합니다."),
        ("2단계 — 인코딩",
         "컨텍스트 블록은 컨텍스트 인코더(ViT)로, "
         "타깃 블록은 EMA(Exponential Moving Average)로 업데이트되는 타깃 인코더로 각각 인코딩합니다."),
        ("3단계 — 예측",
         "예측기는 컨텍스트 표현과 타깃 블록의 위치 정보를 입력받아 "
         "타깃 블록의 표현을 잠재 공간에서 예측합니다."),
        ("4단계 — 손실 계산",
         "예측된 표현과 타깃 인코더가 생성한 실제 표현 사이의 L2 손실을 최소화합니다. "
         "이 과정에서 픽셀 공간으로의 디코딩은 일어나지 않습니다."),
    ]
    for title, desc in steps:
        story.append(Paragraph(f"<b>{title}</b>", S["h3"]))
        story.append(Paragraph(desc, S["body"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("예측기의 세계 모델 관점", S["h2"]))
    story.append(Paragraph(
        "I-JEPA의 예측기는 정적 이미지에서 공간적 불확실성을 모델링하는 "
        "<b>원시적(primitive) 세계 모델</b>로 해석할 수 있습니다. "
        "이 모델은 보이지 않는 영역에 대한 고수준 정보(의미론적 내용)를 예측하며, "
        "확률적 디코더를 학습하면 예측 표현을 스케치 형태로 시각화할 수 있습니다. "
        "예를 들어, 개의 머리·늑대의 앞다리·건물의 반대편 등을 올바른 포즈로 예측합니다.",
        S["body"]))
    story.append(PageBreak())

    # ── 3. 핵심 개념 ──────────────────────────────────────────
    story.append(Paragraph("3. 핵심 개념 정리", S["section"]))
    story.append(Spacer(1, 3*mm))

    concepts = [
        ("JEPA\n(Joint-Embedding\nPredictive Arch.)",
         "Yann LeCun이 제안한 프레임워크. "
         "두 표현 공간을 결합하여 미래/가려진 부분을 예측.\n"
         "생성 모델과 달리 픽셀 재구성 없이 의미론적 학습 가능."),
        ("잠재 공간 예측\n(Latent Space\nPrediction)",
         "픽셀이 아닌 인코더의 출력(표현 벡터)을 예측 대상으로 삼음.\n"
         "불필요한 세부 정보(텍스처·노이즈) 학습을 억제."),
        ("EMA 타깃 인코더\n(EMA Target\nEncoder)",
         "타깃 인코더는 역전파로 직접 학습되지 않고,\n"
         "컨텍스트 인코더 가중치의 지수이동평균으로 업데이트됨.\n"
         "표현 붕괴(representation collapse) 방지."),
        ("멀티-블록 마스킹\n(Multi-block\nMasking)",
         "여러 개의 큰 블록을 마스킹 타깃으로 사용.\n"
         "MAE 등 기존 방법 대비 더 의미론적 단위의 예측 유도."),
        ("ViT 백본\n(Vision Transformer)",
         "컨텍스트/타깃 인코더 모두 Vision Transformer 사용.\n"
         "ViT-H/14 기준 ImageNet-1K 300 에폭 사전학습."),
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

    model_data = [["아키텍처", "패치 크기", "해상도", "에폭", "데이터셋"]]
    models = [
        ("ViT-H", "14×14", "224×224", "300", "ImageNet-1K"),
        ("ViT-H", "16×16", "448×448", "300", "ImageNet-1K"),
        ("ViT-H", "14×14", "224×224", "66",  "ImageNet-22K"),
        ("ViT-g", "16×16", "224×224", "44",  "ImageNet-22K"),
    ]
    for row in models:
        model_data.append([Paragraph(c, S["body"]) for c in row])

    mt = Table(model_data, colWidths=[30*mm, 28*mm, 28*mm, 20*mm, 56*mm])
    mt.setStyle(TableStyle([
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
    story.append(mt)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "모든 체크포인트는 facebookresearch/ijepa GitHub 저장소에서 다운로드할 수 있습니다.",
        S["body"]))
    story.append(PageBreak())

    # ── 5. 빠른 시작 ──────────────────────────────────────────
    story.append(Paragraph("5. 빠른 시작 (Quickstart)", S["section"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("환경 요구사항", S["h2"]))
    for req in [
        "Python 3.8 이상",
        "PyTorch 2.0",
        "torchvision",
        "기타: pyyaml, numpy, opencv, submitit",
    ]:
        story.append(Paragraph(f"• {req}", S["bullet"]))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph("단일 GPU 사전학습", S["h2"]))
    story.append(Paragraph(
        "로컬 머신에서 단일 또는 다중 GPU로 I-JEPA 사전학습을 실행합니다. "
        "모든 실험 파라미터는 커맨드라인 인자가 아닌 <b>config 파일</b>로 지정합니다.",
        S["body"]))
    story.append(Preformatted(
"""python main.py \\
  --fname configs/in1k_vith14_ep300.yaml \\
  --devices cuda:0 cuda:1 cuda:2""", S["code"]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("다중 노드 분산 학습 (SLURM)", S["h2"]))
    story.append(Paragraph(
        "16개의 A100 80G GPU로 ImageNet-1K ViT-H/14 사전학습 예시입니다. "
        "분산 학습은 <b>submitit</b>을 사용하며 SLURM 클러스터를 지원합니다.",
        S["body"]))
    story.append(Preformatted(
"""python main_distributed.py \\
  --fname configs/in1k_vith14_ep300.yaml \\
  --folder $path_to_submitit_logs \\
  --partition $slurm_partition \\
  --nodes 2 --tasks-per-node 8 \\
  --time 1000""", S["code"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "※ ViT-H/14 config는 유효 배치 크기 2048을 위해 16개 A100 80G GPU 권장.",
        style("note", fontSize=8, leading=12, textColor=colors.HexColor("#888888"))))
    story.append(PageBreak())

    # ── 6. 성능 ────────────────────────────────────────────────
    story.append(Paragraph("6. 성능 (Evaluations)", S["section"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "I-JEPA는 <b>계산 효율성</b>과 <b>표현 품질</b> 두 측면에서 뛰어난 성능을 보입니다. "
        "여러 뷰(view) 생성을 위한 데이터 증강 오버헤드가 없으며, "
        "컨텍스트 블록만 컨텍스트 인코더를 통과하므로 계산량이 절감됩니다.",
        S["body"]))
    story.append(Spacer(1, 2*mm))

    story.append(Paragraph("주요 평가 결과", S["h2"]))
    eval_data = [["평가 방식", "특징"]]
    evals = [
        ("1% 레이블 평가\n(1% Label Eval)",
         "ImageNet 1% 레이블만 사용한 선형/미세조정 평가.\n"
         "적은 레이블로도 강력한 표현 학습을 입증."),
        ("선형 평가\n(Linear Eval)",
         "인코더를 고정하고 선형 분류기만 학습.\n"
         "MAE, data2vec 등 대비 우수한 오프더셸프 성능."),
    ]
    for name, desc in evals:
        eval_data.append([
            Paragraph(name, S["label"]),
            Paragraph(desc.replace("\n", "<br/>"), S["body"])
        ])
    et = Table(eval_data, colWidths=[42*mm, 120*mm])
    et.setStyle(TableStyle([
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
    story.append(et)
    story.append(PageBreak())

    # ── 7. 인용 ────────────────────────────────────────────────
    story.append(Paragraph("7. 인용 (Citation)", S["section"]))
    story.append(Spacer(1, 3*mm))
    story.append(Preformatted(
"""@article{assran2023self,
  title   = {Self-Supervised Learning from Images with a
             Joint-Embedding Predictive Architecture},
  author  = {Assran, Mahmoud and Duval, Quentin and Misra, Ishan
             and Bojanowski, Piotr and Vincent, Pascal
             and Rabbat, Michael and LeCun, Yann and Ballas, Nicolas},
  journal = {arXiv preprint arXiv:2301.08243},
  year    = {2023}
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
