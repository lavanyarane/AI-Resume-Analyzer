"""
text_cleaner.py

Cleans and preprocesses resume text.
"""

import re


def clean_text(text):
    """
    Clean extracted resume text.
    """

    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove phone numbers
    text = re.sub(r"\+?\d[\d\s\-()]{8,}", " ", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_resume_sections(text):
    """
    Detect important resume sections.
    """

    text = text.lower()

    sections = [
        "education",
        "skills",
        "projects",
        "experience",
        "internship",
        "certifications",
        "achievements",
        "languages",
        "objective",
        "summary"
    ]

    found = []

    for section in sections:
        if section in text:
            found.append(section.title())

    return found


if __name__ == "__main__":

    sample = """
    JOHN DOE

    Email: john@gmail.com
    Phone: +91-9876543210

    EDUCATION

    B.Tech Computer Science

    SKILLS

    Python, SQL, Machine Learning, Power BI

    PROJECTS

    AI Resume Analyzer

    EXPERIENCE

    Internship at ABC Pvt Ltd
    """

    cleaned = clean_text(sample)

    print(cleaned)

    print(get_resume_sections(sample))