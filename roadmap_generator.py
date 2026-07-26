"""
roadmap_generator.py

Generates a personalized learning roadmap
based on missing skills.
"""

ROADMAP = {

    "Python": "Complete Python basics and practice 50 coding problems.",
    "SQL": "Learn SQL queries, joins, subqueries, and database design.",
    "Excel": "Master formulas, Pivot Tables, Charts, and Data Cleaning.",
    "Power BI": "Build interactive dashboards using Power BI Desktop.",
    "Tableau": "Create visual dashboards and business reports.",
    "Pandas": "Learn data manipulation using Pandas.",
    "NumPy": "Practice arrays, matrix operations, and numerical computing.",
    "Matplotlib": "Learn data visualization using Matplotlib.",
    "Seaborn": "Create statistical visualizations.",
    "Scikit-learn": "Learn machine learning algorithms and model evaluation.",
    "Machine Learning": "Study supervised and unsupervised learning concepts.",
    "Deep Learning": "Learn Neural Networks using TensorFlow/Keras.",
    "TensorFlow": "Build deep learning models using TensorFlow.",
    "PyTorch": "Build AI models using PyTorch.",
    "NLP": "Study Natural Language Processing fundamentals.",
    "Transformers": "Learn HuggingFace Transformers library.",
    "OpenCV": "Build Computer Vision projects using OpenCV.",
    "YOLO": "Learn real-time object detection with YOLO.",
    "Docker": "Containerize Python applications using Docker.",
    "FastAPI": "Build REST APIs using FastAPI.",
    "Flask": "Develop web applications using Flask.",
    "Git": "Learn version control using Git and GitHub.",
    "GitHub": "Push projects and collaborate using GitHub.",
    "Linux": "Learn Linux commands and shell scripting.",
    "AWS": "Learn EC2, S3, IAM, and cloud deployment.",
    "Azure": "Study Microsoft Azure fundamentals.",
    "GCP": "Learn Google Cloud Platform basics.",
    "Streamlit": "Build ML web applications using Streamlit.",
    "HTML": "Learn webpage structure using HTML5.",
    "CSS": "Style web pages using CSS3.",
    "JavaScript": "Learn JavaScript fundamentals.",
    "React": "Build frontend applications using React.",
    "Node.js": "Develop backend APIs using Node.js.",
    "MongoDB": "Learn NoSQL database concepts.",
    "MySQL": "Study relational database management.",
    "PostgreSQL": "Learn advanced SQL using PostgreSQL."
}


def generate_roadmap(missing_skills):
    """
    Creates a 4-week roadmap from missing skills.
    """

    roadmap = {}

    if len(missing_skills) == 0:

        roadmap["Congratulations"] = (
            "Your resume already matches this role very well!"
        )

        return roadmap

    week = 1

    for skill in missing_skills:

        if skill in ROADMAP:

            roadmap[f"Week {week}"] = (
                f"{skill}: {ROADMAP[skill]}"
            )

        else:

            roadmap[f"Week {week}"] = (
                f"Learn the fundamentals of {skill}."
            )

        week += 1

        if week > 4:
            break

    return roadmap


if __name__ == "__main__":

    missing = [
        "Docker",
        "FastAPI",
        "AWS",
        "Git"
    ]

    plan = generate_roadmap(missing)

    for week, task in plan.items():

        print(week, ":", task)