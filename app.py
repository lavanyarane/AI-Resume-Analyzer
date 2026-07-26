import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile
import os

from resume_parser import extract_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import (
    load_job_roles,
    calculate_match_scores,
    get_missing_skills
)
from roadmap_generator import generate_roadmap
from report_generator import generate_report
from ats_score import calculate_ats_score

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ---------------- LOAD CSS ---------------- #

def load_css():
    if os.path.exists("assets/styles.css"):
        with open("assets/styles.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

# ---------------- SIDEBAR ---------------- #

with st.sidebar:
    st.title("🤖 AI Resume Analyzer")

    st.markdown("---")

    st.write("### Features")

    st.success("Resume Parsing")
    st.success("Skill Detection")
    st.success("ATS Score")
    st.success("Job Recommendation")
    st.success("Learning Roadmap")
    st.success("PDF Report")

# ---------------- HEADER ---------------- #

st.markdown("""
<div class='glass'>
<h1>🤖 AI Resume Analyzer</h1>
<h4>Upload your resume and receive AI-powered career insights.</h4>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_file:

    ext = "." + uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:

        tmp.write(uploaded_file.read())

        file_path = tmp.name

    # -------- Parse Resume -------- #

    resume_text = extract_text(file_path)

    cleaned_text = clean_text(resume_text)

    skills = extract_skills(cleaned_text)

    jobs = load_job_roles()

    scores = calculate_match_scores(
        cleaned_text,
        jobs
    )

    score_df = pd.DataFrame(scores)

    ats_score, ats_feedback = calculate_ats_score(
        cleaned_text,
        skills
    )

    best_match = score_df.iloc[0]["Score"]

    # Final Score

    final_score = round(
        best_match * 0.7 + ats_score * 0.3,
        1
    )

    # ---------------- KPI ---------------- #

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Skills", len(skills))
    c2.metric("ATS", f"{ats_score}%")
    c3.metric("Match", f"{best_match}%")
    c4.metric("Final", f"{final_score}%")

    st.markdown("---")

    # ---------------- GAUGE ---------------- #

    gauge = go.Figure(go.Indicator(

        mode="gauge+number",

        value=final_score,

        number={"suffix":"%"},

        title={"text":"Overall Resume Score"},

        gauge={

            "axis":{"range":[0,100]},

            "bar":{"color":"royalblue"},

            "steps":[

                {"range":[0,40],"color":"red"},

                {"range":[40,70],"color":"orange"},

                {"range":[70,100],"color":"green"}

            ]

        }

    ))

    gauge.update_layout(height=350)

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    # ---------------- SKILLS ---------------- #

    st.subheader("💻 Detected Skills")

    html = ""

    for skill in skills:

        html += f'<span class="skill">{skill}</span> '

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------- TOP ROLES ---------------- #

    st.subheader("🏆 Top Job Recommendations")

    top3 = score_df.head(3)

    medals = ["🥇","🥈","🥉"]

    for i,row in top3.iterrows():

        st.markdown(f"""
<div class='role'>
<h3>{medals[i]} {row['Role']}</h3>
<h2>{row['Score']}%</h2>
</div>
""",unsafe_allow_html=True)
            # ---------------- CHARTS ---------------- #

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        pie = px.pie(
            score_df.head(5),
            values="Score",
            names="Role",
            hole=0.45,
            title="Top Matching Roles"
        )

        pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    with col2:

        bar = px.bar(
            score_df.head(5),
            x="Role",
            y="Score",
            color="Score",
            text="Score",
            title="Role Match Score"
        )

        bar.update_layout(
            xaxis_title="Job Role",
            yaxis_title="Match %",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            bar,
            use_container_width=True
        )

    # ---------------- TARGET ROLE ---------------- #

    st.markdown("---")

    target_role = st.selectbox(
        "🎯 Select Target Role",
        score_df["Role"]
    )

    missing = get_missing_skills(
        target_role,
        skills,
        jobs
    )

    # ---------------- MISSING SKILLS ---------------- #

    st.subheader("❌ Missing Skills")

    if missing:

        cols = st.columns(3)

        for i, skill in enumerate(missing):

            cols[i % 3].warning(skill)

    else:

        st.success("🎉 No missing skills found!")

    # ---------------- ATS FEEDBACK ---------------- #

    st.markdown("---")

    st.subheader("🤖 ATS Suggestions")

    if ats_feedback:

        for item in ats_feedback:
            st.info("• " + item)

    else:

        st.success("Excellent! Your resume is ATS-friendly.")

    # ---------------- LEARNING ROADMAP ---------------- #

    st.markdown("---")

    st.subheader("🗺️ Learning Roadmap")

    roadmap = generate_roadmap(missing)

    for week, task in roadmap.items():

        with st.expander(week):

            st.write(task)

    # ---------------- PDF REPORT ---------------- #

    st.markdown("---")

    report_path = generate_report(
        uploaded_file.name,
        skills,
        score_df,
        target_role,
        missing,
        roadmap
    )

    with open(report_path, "rb") as pdf:

        st.download_button(
            "📄 Download PDF Report",
            pdf,
            file_name="Resume_Report.pdf",
            mime="application/pdf"
        )

    # ---------------- AI SUMMARY ---------------- #

    st.markdown("---")

    st.subheader("🤖 AI Career Summary")

    if final_score >= 85:

        st.success(f"""
### Excellent Resume ⭐

**Overall Score:** {final_score}%

You have a strong resume for the **{target_role}** role.

Continue building advanced projects and preparing for technical interviews.
""")

    elif final_score >= 65:

        st.warning(f"""
### Good Resume 👍

**Overall Score:** {final_score}%

Your profile is good but improving the missing skills will significantly increase your chances.
""")

    else:

        st.error(f"""
### Resume Needs Improvement 📚

**Overall Score:** {final_score}%

Add more technical skills, projects, internships, and certifications to strengthen your resume.
""")

    # ---------------- CLEANUP ---------------- #

    if os.path.exists(file_path):
        os.remove(file_path)

else:

    st.info("📄 Upload a PDF or DOCX resume to start the analysis.")

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown(
    """
    <div style='text-align:center;color:gray'>
        <h4>🤖 AI Resume Analyzer & Job Recommendation System</h4>
        <p>Built with ❤️ using Python, Streamlit, NLP, TF-IDF & Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)