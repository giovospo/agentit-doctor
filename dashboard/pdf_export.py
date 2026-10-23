from io import BytesIO

from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    incidents_count,
    events_count,
    root_causes_count
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AgentIT Doctor Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    data = [
        ["Metric", "Value"],
        ["Incidents", str(incidents_count)],
        ["Events", str(events_count)],
        ["Root Causes", str(root_causes_count)]
    ]

    table = Table(data)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ])
    )

    content.append(table)

    doc.build(content)

    buffer.seek(0)

    return buffer