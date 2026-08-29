from io import BytesIO

from fastapi import HTTPException
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy.orm import Session

from app.db.models.user import ScreeningResult


def get_screening_result(
    db: Session,
    screening_id: int,
):
    result = (
        db.query(ScreeningResult)
        .filter(ScreeningResult.screening_id == screening_id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Screening result not found",
        )

    return result


def _format_value(value):
    if value is None:
        return "Not available"

    if isinstance(value, list):
        if not value:
            return "None"
        return ", ".join(str(item) for item in value)

    return str(value)


def generate_screening_report(
    db: Session,
    screening_id: int,
):
    result = get_screening_result(
        db=db,
        screening_id=screening_id,
    )

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
    )

    story = []

    # Title
    story.append(
        Paragraph(
            "AI Resume Screening Report",
            title_style,
        )
    )

    story.append(Spacer(1, 10))

    # Candidate details
    details = [
        ["Candidate", _format_value(result.candidate_name)],
        ["Job Title", _format_value(result.job_title)],
        ["Match Score", f"{result.match_score}%"],
        ["Experience", _format_value(result.experience)],
        ["Qualification", _format_value(result.qualification)],
        ["Certifications", _format_value(result.certifications)],
    ]

    details_table = Table(
        details,
        colWidths=[130, 350],
    )

    details_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(details_table)

    # Matched skills
    story.append(
        Paragraph(
            "Matched Skills",
            heading_style,
        )
    )

    matched_skills = _format_value(result.matched_skills)

    story.append(
        Paragraph(
            matched_skills,
            normal_style,
        )
    )

    # Missing skills
    story.append(
        Paragraph(
            "Missing Skills",
            heading_style,
        )
    )

    missing_skills = _format_value(result.missing_skills)

    story.append(
        Paragraph(
            missing_skills,
            normal_style,
        )
    )

    # Recommendation
    story.append(
        Paragraph(
            "Recommendation",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            _format_value(result.recommendation),
            normal_style,
        )
    )

    # Summary
    story.append(
        Paragraph(
            "Summary",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            _format_value(result.summary),
            normal_style,
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer