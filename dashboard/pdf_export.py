from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf(
    incidents_count,
    events_count,
    root_causes_count
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "AgentIT Doctor Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    summary = [
        ["Metric", "Value"],
        ["Incidents", str(incidents_count)],
        ["Events", str(events_count)],
        ["Root Causes", str(root_causes_count)]
    ]

    table = Table(summary)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
    )

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return buffer.getvalue()