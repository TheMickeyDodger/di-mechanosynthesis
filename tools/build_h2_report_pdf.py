#!/usr/bin/env python3
"""Build the PDF summary of the H2-A-01 result report from marked blocks of the report.

This script is NOT standard-library only: it needs the third-party package reportlab, which this repository does not
provide and which it does not install. The committed PDF was built with Python 3.12.14 and reportlab 4.4.9 from a runtime
that already existed on the build host (nothing was installed and no dependency was changed), and was checked with
Poppler 26.07.0 (pdftoppm, pdftotext, pdfinfo, pdffonts); those versions are recorded in provenance/EXPORT-MANIFEST.md.

It is postprocess-only: it reads docs/learning/h2/H2-A-01-RESULT-REPORT.md and the committed PNG figures in docs/figures/,
runs no engine and computes no chemistry. The PDF is a DERIVED SUMMARY, and says so on its first page together with the
SHA256 of the report it was derived from, computed here from the report file. It reproduces only the blocks of the report that
sit between "<!-- pdf:begin NAME -->" and "<!-- pdf:end NAME -->" markers, in the order of the report, in the report's own
wording, so that no statement appears only in the PDF; the complete tables stay in the full report. A small Markdown subset is
converted (headings, paragraphs, bullet and numbered lists, one image per line). The text must be ASCII. The body is set in
10 pt Bitstream Vera Sans, which ships inside reportlab and is embedded as subsets; Courier (standard, not embedded) is used for
file names and code. Output is deterministic (reportlab invariant mode; its fixed placeholder date is not the build time).

Usage, from the repository root:
    python3 tools/build_h2_report_pdf.py
"""
import hashlib
import os
import re
import struct

import reportlab
from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "docs", "learning", "h2", "H2-A-01-RESULT-REPORT.md")
OUT = os.path.join(ROOT, "docs", "learning", "h2", "H2-A-01-RESULT-REPORT.pdf")
FIG_DIR = os.path.join(ROOT, "docs", "figures")
BLOCKS = ("summary", "fig3", "energy", "fig4", "fig5", "review", "engine", "residuals", "science")
FIG_WIDTH_IN = {"h2-a01-input-geometry": 6.1, "h2-a01-scf-rows": 6.3, "h2-a01-energy-components": 6.0}
BODY_PT, CAPTION_PT = 10.0, 9.0

FONT_DIR = os.path.join(os.path.dirname(reportlab.__file__), "fonts")
for _name, _file in (("Vera", "Vera.ttf"), ("Vera-Bold", "VeraBd.ttf"), ("Vera-Italic", "VeraIt.ttf"), ("Vera-BoldItalic", "VeraBI.ttf")):
    pdfmetrics.registerFont(TTFont(_name, os.path.join(FONT_DIR, _file)))
for _bold, _italic, _name in ((0, 0, "Vera"), (1, 0, "Vera-Bold"), (0, 1, "Vera-Italic"), (1, 1, "Vera-BoldItalic")):
    addMapping("Vera", _bold, _italic, _name)

INK, TEAL, MUTED = colors.HexColor("#1f1f1f"), colors.HexColor("#127c78"), colors.HexColor("#5a5a5a")
LEFT = RIGHT = 0.6 * inch
FRAME_W = letter[0] - LEFT - RIGHT

BODY = ParagraphStyle("body", fontName="Vera", fontSize=BODY_PT, leading=13.0, textColor=INK, spaceAfter=3.5)
CAPTION = ParagraphStyle("caption", parent=BODY, fontSize=CAPTION_PT, leading=11.8, spaceAfter=7)
BOX = ParagraphStyle("box", parent=BODY, fontSize=9, leading=12, spaceAfter=0)
H1 = ParagraphStyle("h1", fontName="Vera-Bold", fontSize=15.5, leading=19, textColor=INK, spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="Vera-Bold", fontSize=12.5, leading=16, textColor=TEAL, spaceBefore=5, spaceAfter=3, keepWithNext=1)
H3 = ParagraphStyle("h3", fontName="Vera-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=6, spaceAfter=3, keepWithNext=1)
ITEM = ParagraphStyle("item", parent=BODY, leftIndent=16, bulletIndent=2, spaceAfter=4)


def inline(text, code_size=BODY_PT - 1.0):
    out = []
    for i, part in enumerate(text.split("`")):
        part = part.replace("\\|", "|").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if i % 2:
            out.append('<font face="Courier" size="%s">%s</font>' % (code_size, part))
        else:
            part = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r"\1", part)
            out.append(re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", part))
    return "".join(out)


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG: " + path
    return struct.unpack(">II", head[16:24])


def convert(block):
    story, para, items = [], [], []
    pending_image = None

    def flush_para():
        nonlocal pending_image
        if para:
            text = " ".join(para)
            if pending_image is not None:                   # heading, image and caption stay on one page
                group = [pending_image, Paragraph(inline(text, CAPTION_PT - 1.0), CAPTION)]
                if story and isinstance(story[-1], Paragraph) and story[-1].style.name in ("h2", "h3"):
                    group.insert(0, story.pop())
                story.append(KeepTogether(group))
                pending_image = None
            else:
                story.append(Paragraph(inline(text), BODY))
            para.clear()

    def flush_items():
        for bullet, lines in items:
            story.append(Paragraph(inline(" ".join(lines)), ITEM, bulletText=bullet))
        items.clear()

    for line in block.strip("\n").split("\n"):
        assert not line.startswith("|"), "tables are not reproduced in the PDF summary: " + line[:40]
        m = re.match(r"^!\[[^\]]*\]\(([^)]+)\)\s*$", line)
        if m:
            flush_para(); flush_items()
            name = os.path.splitext(os.path.basename(m.group(1)))[0]
            path = os.path.join(FIG_DIR, name + ".png")
            w, h = png_size(path)
            width = FIG_WIDTH_IN[name] * inch
            pending_image = Image(path, width=width, height=width * h / w)
            continue
        if line.startswith("### "):
            flush_para(); flush_items(); story.append(Paragraph(inline(line[4:]), H3)); continue
        if line.startswith("## "):
            flush_para(); flush_items(); story.append(Paragraph(inline(line[3:]), H2)); continue
        m = re.match(r"^(- |\d+\.\s)(.*)$", line)
        if m:
            flush_para()
            items.append(("-" if m.group(1) == "- " else m.group(1).strip(), [m.group(2).strip()]))
            continue
        if line.startswith(" ") and items and line.strip():
            items[-1][1].append(line.strip()); continue
        if not line.strip():
            flush_para(); flush_items(); continue
        flush_items(); para.append(line.strip())
    flush_para(); flush_items()
    if pending_image is not None:
        story.append(pending_image)
    return story


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._states = []

    def showPage(self):
        self._states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._states)
        for state in self._states:
            self.__dict__.update(state)
            self.setFont("Vera", 8)
            self.setFillColor(MUTED)
            self.drawString(LEFT, 0.42 * inch, "Unpublished research note - H2-A-01: RHF/STO-3G at a fixed 1.4 bohr separation, single point")
            self.drawRightString(letter[0] - RIGHT, 0.42 * inch, "Page %d of %d" % (self._pageNumber, total))
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


def main():
    raw = open(REPORT, "rb").read()
    text = raw.decode("utf-8")
    text.encode("ascii")
    digest = hashlib.sha256(raw).hexdigest()
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    status = re.search(r"^\*\*Status\.\*\*.*?(?=\n\n)", text, re.S | re.M).group(0).replace("\n", " ")
    blocks = {}
    for m in re.finditer(r"<!-- pdf:begin (\w+) -->\n(.*?)<!-- pdf:end \1 -->", text, re.S):
        blocks[m.group(1)] = m.group(2)
    assert tuple(blocks) == BLOCKS, "unexpected block list: %r" % (tuple(blocks),)
    label = ("<b>Derived summary</b> of the full report <font face=\"Courier\" size=\"8\">docs/learning/h2/H2-A-01-RESULT-REPORT.md</font>, "
             "SHA256 <font face=\"Courier\" size=\"7.6\">%s</font>, listed in <font face=\"Courier\" size=\"8\">provenance/EXPORT-MANIFEST.md</font>. "
             "It reproduces marked blocks of the report in the report's own wording; no statement appears only here. Tables and detail "
             "are in the full report; section numbers are those of the full report." % digest)
    box = Table([[Paragraph(label, BOX)]], colWidths=[FRAME_W])
    box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, TEAL), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f2f6f6")),
                             ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                             ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story = [Paragraph(inline(title), H1), Paragraph(inline(status), BODY), box, Spacer(1, 4)]
    for name in BLOCKS:
        story.extend(convert(blocks[name]))
    doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=LEFT, rightMargin=RIGHT, topMargin=0.5 * inch, bottomMargin=0.62 * inch,
                            title=title, author="di-mechanosynthesis", subject="Derived summary of one recorded single-point RHF/STO-3G "
                            "value at a fixed 1.4 bohr separation", keywords="derived summary; source report sha256 " + digest,
                            creator="tools/build_h2_report_pdf.py", invariant=1)
    doc.build(story, canvasmaker=NumberedCanvas)
    print("blocks=%d report_sha256=%s output=%s" % (len(blocks), digest, os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
