"""
Aurora 논문 폴더의 문서 파일들을 하나의 PDF로 변환
출력: my-folder/S/aurora.pdf
"""

import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    HRFlowable, PageBreak, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── 경로 설정 ───────────────────────────────────────────────
BASE   = "C:/Discovery/Cosmo/dev/lab/time-series/aurora"
DOC    = os.path.join(BASE, "doc")
OUTPUT = "C:/Discovery/Cosmo/dev/lab/my-folder/S/aurora.pdf"

MD_FILES = [
    (os.path.join(BASE, "README.md"),                                        "Aurora — Main"),
    (os.path.join(BASE, "TFB/characteristics_extractor/Readme_en.md"),      "TFB — Characteristics Extractor"),
    (os.path.join(BASE, "TFB/characteristics_extractor/Readme_chn.md"),     "TFB — 특성 추출기 (중문)"),
]

# ── 스타일 정의 ──────────────────────────────────────────────
styles = getSampleStyleSheet()

S = {
    "h1": ParagraphStyle("h1", parent=styles["Heading1"],
              fontSize=18, leading=24, spaceAfter=8,
              textColor=colors.HexColor("#1a1a2e")),
    "h2": ParagraphStyle("h2", parent=styles["Heading2"],
              fontSize=14, leading=18, spaceBefore=10, spaceAfter=4,
              textColor=colors.HexColor("#16213e")),
    "h3": ParagraphStyle("h3", parent=styles["Heading3"],
              fontSize=11, leading=15, spaceBefore=6, spaceAfter=3,
              textColor=colors.HexColor("#0f3460")),
    "body": ParagraphStyle("body", parent=styles["Normal"],
              fontSize=9, leading=14, spaceAfter=4),
    "code": ParagraphStyle("code", parent=styles["Code"],
              fontSize=7.5, leading=11, backColor=colors.HexColor("#f4f4f4"),
              leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4,
              fontName="Courier"),
    "section": ParagraphStyle("section", parent=styles["Heading1"],
              fontSize=20, leading=26, spaceAfter=12,
              textColor=colors.white,
              backColor=colors.HexColor("#1a1a2e"),
              borderPadding=(6, 8, 6, 8)),
}

# ── 이미지 삽입 헬퍼 ─────────────────────────────────────────
def insert_image(path, width_mm=120):
    if not os.path.exists(path):
        return None
    try:
        img = Image(path)
        ratio = img.imageHeight / img.imageWidth
        w = width_mm * mm
        return Image(path, width=w, height=w * ratio)
    except Exception:
        return None

# ── 마크다운 → Flowable 변환 ─────────────────────────────────
def md_to_flowables(md_text, base_dir):
    flowables = []
    lines     = md_text.splitlines()
    i         = 0

    while i < len(lines):
        line = lines[i]

        # 코드 블록
        if line.strip().startswith("```"):
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_text = "\n".join(code_lines)
            flowables.append(Preformatted(code_text, S["code"]))
            i += 1
            continue

        # 인라인 이미지  ![alt](src)
        img_match = re.match(r'!\[.*?\]\((.+?)\)', line.strip())
        if img_match:
            src = img_match.group(1)
            img_path = src if os.path.isabs(src) else os.path.join(base_dir, src)
            img = insert_image(img_path, width_mm=130)
            if img:
                flowables.append(Spacer(1, 4))
                flowables.append(img)
                flowables.append(Spacer(1, 4))
            i += 1
            continue

        # HTML img 태그
        html_img = re.search(r'<img[^>]*src=["\']([^"\']+)["\']', line)
        if html_img:
            src = html_img.group(1)
            img_path = src if os.path.isabs(src) else os.path.join(base_dir, src)
            img = insert_image(img_path, width_mm=40)
            if img:
                flowables.append(img)
            i += 1
            continue

        # div align 태그 (이미지 래퍼) → 다음 줄에서 이미지 처리
        if re.match(r'\s*<div', line) or re.match(r'\s*</div>', line):
            i += 1
            continue

        # 배지/shield.io 링크 무시
        if "img.shields.io" in line or "badge" in line.lower():
            i += 1
            continue

        # 헤딩
        h1 = re.match(r'^# (.+)', line)
        h2 = re.match(r'^## (.+)', line)
        h3 = re.match(r'^### (.+)', line)
        h4 = re.match(r'^#{4,} (.+)', line)

        # 텍스트 정리 (인라인 마크다운 제거)
        def clean(t):
            t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)   # 링크
            t = re.sub(r'`([^`]+)`', r'\1', t)                 # 인라인 코드
            t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)   # 굵게
            t = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', t)        # 이탤릭
            t = re.sub(r'<[^>]+>', lambda m: m.group(0)
                       if m.group(0).lower() in ('<b>','</b>','<i>','</i>')
                       else '', t)
            return t.strip()

        if h1:
            flowables.append(Paragraph(clean(h1.group(1)), S["h1"]))
        elif h2:
            flowables.append(Spacer(1, 4))
            flowables.append(HRFlowable(width="100%", thickness=0.5,
                                         color=colors.HexColor("#cccccc")))
            flowables.append(Paragraph(clean(h2.group(1)), S["h2"]))
        elif h3:
            flowables.append(Paragraph(clean(h3.group(1)), S["h3"]))
        elif h4:
            flowables.append(Paragraph(clean(h4.group(1)), S["h3"]))
        elif line.strip().startswith(("- ", "* ", "+ ")):
            text = clean(line.strip()[2:])
            flowables.append(Paragraph(f"• {text}", S["body"]))
        elif re.match(r'^\d+\. ', line.strip()):
            text = clean(re.sub(r'^\d+\. ', '', line.strip()))
            flowables.append(Paragraph(f"  {text}", S["body"]))
        elif line.strip() == "" or line.strip() == "---":
            flowables.append(Spacer(1, 4))
        elif line.strip():
            flowables.append(Paragraph(clean(line.strip()), S["body"]))

        i += 1

    return flowables

# ── PDF 생성 ─────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm,  bottomMargin=18*mm,
    )

    story = []

    # 표지
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("Aurora", ParagraphStyle("cover_title",
        fontSize=36, leading=44, alignment=TA_CENTER,
        textColor=colors.HexColor("#1a1a2e"), fontName="Helvetica-Bold")))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "Towards Universal Generative Multimodal Time Series Forecasting",
        ParagraphStyle("cover_sub", fontSize=13, leading=18,
            alignment=TA_CENTER, textColor=colors.HexColor("#444444"))))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("ICLR 2026",
        ParagraphStyle("cover_conf", fontSize=11, alignment=TA_CENTER,
            textColor=colors.HexColor("#e94560"))))
    logo = insert_image(os.path.join(DOC, "logo.png"), width_mm=30)
    if logo:
        story.append(Spacer(1, 8*mm))
        story.append(logo)
    story.append(PageBreak())

    # 각 문서 삽입
    for path, title in MD_FILES:
        if not os.path.exists(path):
            continue

        # 섹션 구분 헤더
        story.append(Paragraph(title, S["section"]))
        story.append(Spacer(1, 4*mm))

        with open(path, encoding="utf-8") as f:
            md_text = f.read()

        base_dir = os.path.dirname(path)
        story.extend(md_to_flowables(md_text, base_dir))
        story.append(PageBreak())

    doc.build(story)
    print(f"PDF 생성 완료: {OUTPUT}")

if __name__ == "__main__":
    build_pdf()
