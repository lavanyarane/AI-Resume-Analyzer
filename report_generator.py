"""
Professional PDF Report Generator
"""

import os
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

REPORT_DIR = "reports"

os.makedirs(REPORT_DIR, exist_ok=True)


def generate_report(
    resume_name,
    skills,
    score_df,
    target_role,
    missing_skills,
    roadmap,
    ats_score=0,
    final_score=0
):

    report_path = os.path.join(
        REPORT_DIR,
        "Resume_Report.pdf"
    )

    doc = SimpleDocTemplate(report_path)

    styles = getSampleStyleSheet()

    story = []

    # ------------------------------------------------

    story.append(
        Paragraph(
            "<font size=22><b>AI Resume Analysis Report</b></font>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # ------------------------------------------------

    info = [

        ["Resume", resume_name],

        ["Target Role", target_role],

        ["ATS Score", f"{ats_score}%"],

        ["Final Resume Score", f"{final_score}%"]

    ]

    table = Table(info, colWidths=[150, 300])

    table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 0), (0, -1), colors.lightblue),

            ("BACKGROUND", (1, 0), (1, -1), colors.whitesmoke),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

        ])

    )

    story.append(table)

    story.append(Spacer(1, 18))

    # ------------------------------------------------
    # Skills
    # ------------------------------------------------

    story.append(
        Paragraph(
            "<b>Detected Skills</b>",
            styles["Heading2"]
        )
    )

    if skills:

        story.append(
            Paragraph(
                ", ".join(skills),
                styles["BodyText"]
            )
        )

    else:

        story.append(
            Paragraph(
                "No skills detected.",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    # ------------------------------------------------
    # Top Roles
    # ------------------------------------------------

    story.append(
        Paragraph(
            "<b>Top Job Recommendations</b>",
            styles["Heading2"]
        )
    )

    role_table = [["Role", "Match Score"]]

    for _, row in score_df.head(3).iterrows():

        role_table.append([
            row["Role"],
            f"{row['Score']}%"
        ])

    t = Table(role_table)

    t.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("ALIGN", (0, 0), (-1, -1), "CENTER")

        ])

    )

    story.append(t)

    story.append(Spacer(1, 15))

    # ------------------------------------------------
    # Missing Skills
    # ------------------------------------------------

    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )
    )

    if missing_skills:

        for skill in missing_skills:

            story.append(
                Paragraph(
                    f"• {skill}",
                    styles["BodyText"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No missing skills.",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    # ------------------------------------------------
    # Roadmap
    # ------------------------------------------------

    story.append(
        Paragraph(
            "<b>Learning Roadmap</b>",
            styles["Heading2"]
        )
    )

    for week, task in roadmap.items():

        story.append(
            Paragraph(
                f"<b>{week}</b> : {task}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    # ------------------------------------------------
    # Resume Rating
    # ------------------------------------------------

    if final_score >= 85:

        result = "Excellent Resume"

    elif final_score >= 65:

        result = "Good Resume"

    else:

        result = "Needs Improvement"

    story.append(
        Paragraph(
            "<b>Overall Evaluation</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            result,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # ------------------------------------------------

    story.append(

        Paragraph(

            "<i>This report is generated using NLP, ATS scoring and TF-IDF similarity. It is intended for educational purposes.</i>",

            styles["Italic"]

        )

    )

    doc.build(story)

    return report_path