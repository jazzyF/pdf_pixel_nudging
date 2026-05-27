"""Creates a sample PDF template with labeled boxes to fill in."""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def create_template():
    c = canvas.Canvas("/dev/src/template.pdf", pagesize=letter)
    width, height = letter  # 612 x 792 points

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, height - 60, "SAMPLE FORM TEMPLATE")

    # Draw labeled boxes to simulate form sections
    sections = [
        {"label": "Full Name",       "x": 72,  "y": height - 160, "w": 220, "h": 30},
        {"label": "Date",            "x": 340, "y": height - 160, "w": 200, "h": 30},
        {"label": "Company",         "x": 72,  "y": height - 240, "w": 468, "h": 30},
        {"label": "Address",         "x": 72,  "y": height - 320, "w": 468, "h": 30},
        {"label": "City",            "x": 72,  "y": height - 400, "w": 200, "h": 30},
        {"label": "State",           "x": 310, "y": height - 400, "w": 80,  "h": 30},
        {"label": "ZIP",             "x": 430, "y": height - 400, "w": 110, "h": 30},
        {"label": "Notes / Comments","x": 72,  "y": height - 520, "w": 468, "h": 80},
    ]

    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)

    for s in sections:
        # Draw box
        c.setFillColor(colors.whitesmoke)
        c.rect(s["x"], s["y"], s["w"], s["h"], fill=1, stroke=1)
        # Label above box
        c.setFillColor(colors.grey)
        c.drawString(s["x"], s["y"] + s["h"] + 4, s["label"])

    c.save()
    print("Template created: template.pdf")

create_template()
