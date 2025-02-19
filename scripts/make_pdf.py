"""Render the current protocol as an explicitly marked draft PDF."""

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

root = Path(__file__).resolve().parents[1]
font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
styles = getSampleStyleSheet()
if font.exists():
    pdfmetrics.registerFont(TTFont("DejaVu", str(font)))
    for style in styles.byName.values():
        style.fontName = "DejaVu"
styles["BodyText"].leading = 15
parts = []
for block in (root / "report/protocol.md").read_text().split("\n\n"):
    text = " ".join(block.splitlines())
    if text.startswith("# "):
        style, text = "Title", text[2:]
    elif text.startswith("## "):
        style, text = "Heading2", text[3:]
    else:
        style = "BodyText"
    parts.extend([Paragraph(escape(text), styles[style]), Spacer(1, 9)])


def footer(canvas, document):
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(
        0.7 * inch, 0.4 * inch, "DRAFT PROTOCOL — model results and human review pending"
    )
    canvas.drawRightString(7.6 * inch, 0.4 * inch, str(document.page))


out = root / "report/nigerian-agent-safety-draft.pdf"
SimpleDocTemplate(
    str(out),
    title="Nigerian-language agent safety — draft protocol",
    author="Inioluwa Atanda",
    topMargin=0.6 * inch,
    bottomMargin=0.7 * inch,
).build(parts, onFirstPage=footer, onLaterPages=footer)
print(out)
