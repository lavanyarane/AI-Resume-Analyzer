"""
job_matcher.py

Compares resume with job roles using
TF-IDF + Cosine Similarity.
"""

import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


JOB_FILE = os.path.join("data", "job_roles.csv")


def load_job_roles():
    """
    Load job role dataset.

    Required CSV columns:
    Role
    Skills
    """

    try:
        df = pd.read_csv(JOB_FILE)

        df = df.fillna("")

        return df

    except Exception as e:

        print("Error:", e)

        return pd.DataFrame(
            columns=["Role", "Skills"]
        )


def calculate_match_scores(resume_text, jobs):
    """
    Calculate similarity between resume
    and every job role.
    """

    documents = [resume_text]

    documents.extend(
        jobs["Skills"].tolist()
    )

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf = vectorizer.fit_transform(documents)

    resume_vector = tfidf[0]

    job_vectors = tfidf[1:]

    similarities = cosine_similarity(
        resume_vector,
        job_vectors
    )[0]

    results = []

    for i, score in enumerate(similarities):

        results.append(
            {
                "Role": jobs.iloc[i]["Role"],
                "Score": round(score * 100, 2)
            }
        )

    results = sorted(
        results,
        key=lambda x: x["Score"],
        reverse=True
    )

    return results


def top_roles(results, n=3):
    """
    Return top N roles.
    """

    return results[:n]


def get_missing_skills(
    role,
    detected_skills,
    jobs
):
    """
    Compare detected skills with
    required role skills.
    """

    row = jobs[
        jobs["Role"] == role
    ]

    if row.empty:

        return []

    required = row.iloc[0]["Skills"]

    required = [
        x.strip()
        for x in required.split(",")
    ]

    found = [
        x.lower()
        for x in detected_skills
    ]

    missing = []

    for skill in required:

        if skill.lower() not in found:

            missing.append(skill)

    return missing


def calculate_skill_percentage(
    role,
    detected_skills,
    jobs
):
    """
    Percentage of required skills found.
    """

    row = jobs[
        jobs["Role"] == role
    ]

    if row.empty:

        return 0

    required = [
        x.strip()
        for x in row.iloc[0]["Skills"].split(",")
    ]

    if len(required) == 0:

        return 0

    count = 0

    for skill in required:

        if skill.lower() in [
            x.lower()
            for x in detected_skills
        ]:

            count += 1

    return round(
        count / len(required) * 100,
        2
    )


if __name__ == "__main__":

    jobs = load_job_roles()

    sample_resume = """
    Python SQL Pandas
    Machine Learning
    Docker Git
    Streamlit
    """

    results = calculate_match_scores(
        sample_resume,
        jobs
    )

    print(results)

    print()

    print(
        top_roles(results)
    )