"""
skill_extractor.py

Extracts technical skills from resume text.
"""

import pandas as pd
import os

SKILL_FILE = os.path.join("data", "skills.csv")


def load_skills():
    """
    Load skills from CSV file.
    """

    try:
        df = pd.read_csv(SKILL_FILE)
        return df["Skill"].dropna().tolist()

    except Exception as e:
        print("Error loading skills:", e)
        return []


def extract_skills(text):
    """
    Extract skills from cleaned resume text.
    """

    if not text:
        return []

    text = text.lower()

    skills = load_skills()

    detected = []

    for skill in skills:

        skill_lower = skill.lower()

        # Exact phrase match (supports multi-word skills)
        if skill_lower in text:
            detected.append(skill)

    # Remove duplicates and sort alphabetically
    detected = sorted(list(set(detected)))

    return detected


def skill_categories(skills):
    """
    Group detected skills by category.
    """

    try:
        df = pd.read_csv(SKILL_FILE)

    except:
        return {}

    categories = {}

    for skill in skills:

        row = df[df["Skill"].str.lower() == skill.lower()]

        if not row.empty:

            category = row.iloc[0]["Category"]

            categories.setdefault(category, []).append(skill)

    return categories


if __name__ == "__main__":

    sample = """
    Python SQL Pandas NumPy Machine Learning
    Scikit-learn Docker Git GitHub
    FastAPI Power BI Streamlit AWS
    """

    skills = extract_skills(sample)

    print("Detected Skills:")
    print(skills)

    print("\nCategories:")
    print(skill_categories(skills))