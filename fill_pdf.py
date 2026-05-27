"""
PDF Text Overlay — Proof of Concept
====================================
Strategy:
  1. Define text fields with precise (x, y) coordinates.
  2. Use reportlab to draw that text onto a transparent overlay PDF.
  3. Use pypdf to merge the overlay onto your template.

Coordinate system reminder:
  - Origin (0, 0) is BOTTOM-LEFT of the page.
  - Letter page = 612 pts wide × 792 pts tall  (1 pt = 1/72 inch)
  - To convert inches → points: multiply by 72
      e.g.  1.5 inches from left  = 1.5 * 72 = 108 pts
            2.0 inches from top   = 792 - (2.0 * 72) = 648 pts

Tuning tip:
  - Run with DEBUG_GRID = True to render a coordinate grid + crosshairs
    so you can visually identify exact positions before finalising.
"""

import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter

# ── Page dimensions ────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter   # 612 × 792 pts

# ── Toggle debug grid overlay ──────────────────────────────────────────────────
DEBUG_GRID = True   # Set False for clean output

# ── Define your text fields ────────────────────────────────────────────────────
# Each entry: (text, x, y, font_name, font_size)
# x = distance from LEFT edge  (pts)
# y = distance from BOTTOM edge (pts)  ← remember: bottom-left origin!
TEXT_FIELDS = [
    # text                    x     y      font              size
    ("Jane Doe",              80,   PAGE_H - 148,  "Helvetica",      11),
    ("2026-05-26",            348,  PAGE_H - 148,  "Helvetica",      11),
    ("Acme Corporation",      80,   PAGE_H - 228,  "Helvetica",      11),
    ("123 Main Street, #4",   80,   PAGE_H - 308,  "Helvetica",      11),
    ("Atlanta",               80,   PAGE_H - 388,  "Helvetica",      11),
    ("GA",                    318,  PAGE_H - 388,  "Helvetica",      11),
    ("30301",                 438,  PAGE_H - 388,  "Helvetica",      11),
    ("Please process ASAP.",  80,   PAGE_H - 490,  "Helvetica-Oblique", 10),
]

# ── Helper: draw a debug coordinate grid ──────────────────────────────────────
def draw_debug_grid(c, step=50):
    """Draws a light grid with coordinate labels every `step` points."""
    from reportlab.lib import colors
    c.setStrokeColor(colors.Color(0.75, 0.85, 1.0))   # light blue
    c.setFillColor(colors.Color(0.3, 0.3, 0.8))
    c.setLineWidth(0.3)
    c.setFont("Helvetica", 6)

    for x in range(0, int(PAGE_W) + 1, step):
        c.line(x, 0, x, PAGE_H)
        c.drawString(x + 1, 4, str(x))

    for y in range(0, int(PAGE_H) + 1, step):
        c.line(0, y, PAGE_W, y)
        c.drawString(2, y + 1, str(y))

    # Crosshairs on each text field position
    c.setStrokeColor(colors.red)
    c.setLineWidth(0.8)
    for _, x, y, _, _ in TEXT_FIELDS:
        c.line(x - 6, y, x + 6, y)   # horizontal tick
        c.line(x, y - 6, x, y + 6)   # vertical tick

# ── Build text overlay ─────────────────────────────────────────────────────────
def build_overlay() -> bytes:
    """Returns a single-page PDF (in memory) with only the positioned text."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    if DEBUG_GRID:
        draw_debug_grid(c)

    # Draw each text field
    for text, x, y, font, size in TEXT_FIELDS:
        c.setFont(font, size)
        c.setFillColorRGB(0, 0, 0)      # black text
        c.drawString(x, y, text)

    c.save()
    buf.seek(0)
    return buf.read()

# ── Merge overlay onto template ────────────────────────────────────────────────
def merge_onto_template(template_path: str, output_path: str):
    overlay_bytes = build_overlay()

    template_pdf = PdfReader(template_path)
    overlay_pdf  = PdfReader(io.BytesIO(overlay_bytes))

    writer = PdfWriter()
    template_page = template_pdf.pages[0]
    overlay_page  = overlay_pdf.pages[0]

    # merge_page() draws the overlay ON TOP of the template
    template_page.merge_page(overlay_page)
    writer.add_page(template_page)

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✓ Output saved → {output_path}")
    print(f"  DEBUG_GRID={'ON (grid + crosshairs visible)' if DEBUG_GRID else 'OFF'}")
    print(f"  Fields placed: {len(TEXT_FIELDS)}")

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    merge_onto_template(
        template_path="/home/claude/template.pdf",
        output_path="/mnt/user-data/outputs/filled_form.pdf",
    )