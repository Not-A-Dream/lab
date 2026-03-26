"""
V-JEPA Meta AI Blog 내용을 PDF로 변환
출처: https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/
출력: my-folder/A-data/vjepa_meta_blog.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = "C:/Discovery/Cosmo/dev/lab/my-folder/A-data/vjepa_meta_blog.pdf"

styles = getSampleStyleSheet()

S = {
    "cover_title": ParagraphStyle("cover_title",
        fontSize=36, leading=44, alignment=TA_CENTER,
        textColor=colors.HexColor("#0064e0"), fontName="Helvetica-Bold"),
    "cover_sub": ParagraphStyle("cover_sub",
        fontSize=14, leading=20, alignment=TA_CENTER,
        textColor=colors.HexColor("#444444")),
    "cover_meta": ParagraphStyle("cover_meta",
        fontSize=10, leading=14, alignment=TA_CENTER,
        textColor=colors.HexColor("#888888")),
    "h1": ParagraphStyle("h1", parent=styles["Heading1"],
        fontSize=18, leading=24, spaceAfter=8,
        textColor=colors.HexColor("#0064e0")),
    "h2": ParagraphStyle("h2", parent=styles["Heading2"],
        fontSize=13, leading=18, spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor("#1c1e21")),
    "h3": ParagraphStyle("h3", parent=styles["Heading3"],
        fontSize=11, leading=15, spaceBefore=6, spaceAfter=3,
        textColor=colors.HexColor("#0064e0")),
    "body": ParagraphStyle("body", parent=styles["Normal"],
        fontSize=9.5, leading=15, spaceAfter=5),
    "bullet": ParagraphStyle("bullet", parent=styles["Normal"],
        fontSize=9.5, leading=15, spaceAfter=3, leftIndent=12),
    "highlight": ParagraphStyle("highlight", parent=styles["Normal"],
        fontSize=9.5, leading=15, spaceAfter=5,
        backColor=colors.HexColor("#f0f4ff"),
        leftIndent=10, rightIndent=10,
        borderPadding=(6, 8, 6, 8)),
    "source": ParagraphStyle("source",
        fontSize=7.5, leading=11, alignment=TA_CENTER,
        textColor=colors.HexColor("#aaaaaa")),
}


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"))


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=18*mm, bottomMargin=18*mm,
    )

    story = []

    # ── 표지 ───────────────────────────────────────────────────
    story.append(Spacer(1, 35*mm))
    story.append(Paragraph("V-JEPA", S["cover_title"]))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "Video Joint Embedding Predictive Architecture",
        S["cover_sub"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Yann LeCun · Meta AI Research · 2024",
        S["cover_meta"]))
    story.append(Spacer(1, 6*mm))
    story.append(hr())
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Source: ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/",
        S["source"]))
    story.append(PageBreak())

    # ── 본문 ───────────────────────────────────────────────────

    # 1. 개요
    story.append(Paragraph("Overview", S["h1"]))
    story.append(hr())
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "Meta released <b>Video Joint Embedding Predictive Architecture (V-JEPA)</b>, "
        "a significant advancement toward Yann LeCun's vision of Advanced Machine Intelligence (AMI). "
        "The model learns from unlabeled video data by predicting masked portions in abstract "
        "representation space—rather than reconstructing pixel-level details.",
        S["body"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        'V-JEPA represents <b>"a step toward a more grounded understanding of the world"</b>, '
        "enabling machines to develop internal models similar to human learning processes.",
        S["highlight"]))
    story.append(Spacer(1, 5*mm))

    # 2. Core Innovation
    story.append(Paragraph("Core Innovation", S["h2"]))
    story.append(Spacer(1, 2*mm))

    innovations = [
        ("<b>Abstract Representation Space</b>: Instead of predicting raw pixels, V-JEPA predicts "
         "in a learned embedding space. This forces the model to capture semantic meaning rather than "
         "low-level pixel statistics."),
        ("<b>Spatio-Temporal Masking</b>: The model masks large spatio-temporal video regions, "
         "forcing the system to learn meaningful scene understanding. Blocking both spatial and "
         "temporal areas simultaneously prevents the learning task from becoming trivial."),
        ("<b>Self-Supervised Pre-training</b>: Requires only unlabeled video data for pre-training, "
         "with labels applied afterward for task-specific adaptation—a more efficient methodology "
         "than full fine-tuning."),
        ("<b>Frozen Encoder Evaluation</b>: The same pre-trained encoder can be reused across multiple "
         "downstream tasks without modification, demonstrating strong generalization."),
    ]
    for item in innovations:
        story.append(Paragraph(f"• {item}", S["bullet"]))
        story.append(Spacer(1, 2*mm))

    story.append(Spacer(1, 4*mm))

    # 3. Efficiency
    story.append(Paragraph("Training Efficiency", S["h2"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "V-JEPA achieves training efficiency improvements ranging from <b>1.5x to 6x</b> "
        "compared to previous approaches by working in abstract representation space rather than "
        "reconstructing actual pixels. This reduction in computational overhead enables scaling "
        "to larger video datasets.",
        S["body"]))
    story.append(Spacer(1, 5*mm))

    # 4. Practical Applications
    story.append(Paragraph("Practical Applications", S["h2"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "V-JEPA excels at recognizing <b>fine-grained object interactions</b>, such as distinguishing "
        "between putting down a pen versus pretending to do so. This level of nuanced understanding "
        "is critical for real-world deployment.",
        S["body"]))
    story.append(Spacer(1, 2*mm))

    applications = [
        "Fine-grained action recognition in video",
        "Object interaction understanding",
        "Multi-task adaptation via frozen encoder",
        "Embodied AI (robotics, navigation)",
        "Contextual assistance for augmented reality devices",
    ]
    for app in applications:
        story.append(Paragraph(f"• {app}", S["bullet"]))
    story.append(Spacer(1, 5*mm))

    # 5. Connection to World Models / AMI
    story.append(Paragraph("Connection to World Models &amp; AMI", S["h2"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "V-JEPA is a direct embodiment of Yann LeCun's world model hypothesis: machines should learn "
        "an internal model of the world that can be used for prediction and planning, rather than "
        "purely reactive pattern matching. The joint embedding approach aligns predictions and targets "
        "in a shared latent space, avoiding the need to model every pixel of the future.",
        S["body"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        "<b>Key insight</b>: Predicting in representation space (not pixel space) = more robust, "
        "more efficient, and more generalizable internal world model.",
        S["highlight"]))
    story.append(Spacer(1, 5*mm))

    # 6. Future Directions
    story.append(Paragraph("Future Directions", S["h2"]))
    story.append(Spacer(1, 2*mm))
    future = [
        "Incorporate <b>audio</b> alongside visual content (multimodal extension)",
        "Extend prediction to <b>longer time horizons</b> for planning applications",
        "Scale to larger and more diverse video datasets",
        "Apply to <b>embodied AI</b> and robotics for real-world planning",
        "Explore integration with AR/VR contextual assistance",
    ]
    for f in future:
        story.append(Paragraph(f"• {f}", S["bullet"]))
    story.append(Spacer(1, 5*mm))

    # 7. Relation to I-JEPA
    story.append(Paragraph("Relation to I-JEPA", S["h2"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "V-JEPA extends <b>I-JEPA (Image JEPA)</b> to the video domain. While I-JEPA applies "
        "joint embedding predictive architecture to static images, V-JEPA adds the temporal "
        "dimension, requiring the model to understand how the world evolves over time.",
        S["body"]))

    rows = [
        ("", "I-JEPA", "V-JEPA"),
        ("Modality", "Image (static)", "Video (temporal)"),
        ("Masking", "Spatial patches", "Spatio-temporal blocks"),
        ("Prediction target", "Image embedding", "Video embedding"),
        ("Key challenge", "Spatial semantics", "Temporal dynamics"),
    ]
    story.append(Spacer(1, 3*mm))

    for i, row in enumerate(rows):
        label, col1, col2 = row
        if i == 0:
            line = f"<b>{label:12s}  {col1:25s}  {col2}</b>"
        else:
            line = f"<b>{label:12s}</b>  {col1:25s}  {col2}"
        story.append(Paragraph(line, S["body"]))

    story.append(Spacer(1, 5*mm))

    # 8. License & Access
    story.append(Paragraph("License &amp; Access", S["h2"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "V-JEPA is released under <b>Creative Commons NonCommercial (CC BY-NC)</b> licensing "
        "for research purposes.",
        S["body"]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "• GitHub (I-JEPA): github.com/facebookresearch/ijepa",
        S["bullet"]))
    story.append(Paragraph(
        "• GitHub (V-JEPA 2): github.com/facebookresearch/vjepa2",
        S["bullet"]))
    story.append(Paragraph(
        "• Blog: ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/",
        S["bullet"]))

    story.append(Spacer(1, 10*mm))
    story.append(hr())
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "For research and educational purposes only. Not for commercial use. "
        "Original content copyright Meta AI.",
        S["source"]))

    doc.build(story)
    print(f"PDF 생성 완료: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
