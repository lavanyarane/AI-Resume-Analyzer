"""
ats_score.py

Calculates ATS Resume Score and provides suggestions.
"""

# Keywords that should ideally appear as resume sections
REQUIRED_SECTIONS = [
    "education",
    "skills",
    "projects",
    "experience",
    "internship",
    "certifications"
]


def calculate_ats_score(text, detected_skills):
    """
    Calculate ATS score based on:
    1. Resume sections
    2. Number of detected skills
    3. Resume length

    Returns:
        score (int)
        feedback (list)
    """

    score = 0
    feedback = []

    if not text:
        return 0, ["Resume is empty."]

    text = text.lower()

    # -----------------------------
    # Section Score (40 Marks)
    # -----------------------------
    for section in REQUIRED_SECTIONS:
        if section in text:
            score += 7
        else:
            feedback.append(f"Add a '{section.title()}' section.")

    # -----------------------------
    # Skill Score (40 Marks)
    # -----------------------------
    skill_count = len(detected_skills)

    if skill_count >= 20:
        score += 40
    elif skill_count >= 15:
        score += 35
    elif skill_count >= 10:
        score += 30
    elif skill_count >= 5:
        score += 20
    else:
        score += 10
        feedback.append("Add more technical skills.")

    # -----------------------------
    # Resume Length Score (20 Marks)
    # -----------------------------
    word_count = len(text.split())

    if word_count >= 350:
        score += 20
    elif word_count >= 250:
        score += 15
    elif word_count >= 150:
        score += 10
    else:
        score += 5
        feedback.append("Resume is too short.")

    # Ensure score stays within 0–100
    score = min(score, 100)

    if score >= 85:
        feedback.append("Excellent ATS-friendly resume.")
    elif score >= 70:
        feedback.append("Good resume. Improve missing skills for a higher score.")
    else:
        feedback.append("Resume needs improvement to pass ATS systems.")

    return score, feedback


# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":

    sample_resume = """
    Education
    Skills
    Projects
    Experience

    Python SQL Pandas Machine Learning Docker Git Streamlit
    """

    sample_skills = [
        "Python",
        "SQL",
        "Pandas",
        "Machine Learning",
        "Docker",
        "Git",
        "Streamlit"
    ]

    score, feedback = calculate_ats_score(
        sample_resume,
        sample_skills
    )

    print("ATS Score:", score)

    print("\nFeedback:")

    for item in feedback:
        print("-", item)