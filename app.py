import streamlit as st
import pandas as pd
from modules.resume_parser import extract_text
from modules.skill_extractor import extract_skills
from modules.matching_engine import match_resume_to_job

st.set_page_config(page_title="AIVORA | Resume Matcher", page_icon="🧠", layout="wide")

st.title("🧠 AIVORA")
st.subheader("Intelligent Resume-to-Job Matching")
st.caption("Semantic matching • Explainable skills • Recruiter shortlist • Candidate skill-gap report")

with st.sidebar:
    st.header("Choose workspace")
    mode = st.radio("Workspace", ["Recruiter", "Candidate"])
    st.divider()
    st.caption("Prototype note: scores support human review; they are not hiring decisions.")

job_description = st.text_area(
    "Paste the job description",
    height=220,
    placeholder="Example: We are looking for a Python developer with SQL, machine learning, Git..."
)

if mode == "Recruiter":
    st.markdown("### Recruiter workspace")
    resumes = st.file_uploader(
        "Upload candidate resumes (PDF, DOCX or TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
    if st.button("Analyze and rank candidates", type="primary", disabled=not (job_description.strip() and resumes)):
        rows, details = [], []
        progress = st.progress(0)
        for i, resume in enumerate(resumes):
            try:
                text = extract_text(resume)
                if not text.strip():
                    raise ValueError("No readable text found. If this is a scanned PDF, run OCR first.")
                result = match_resume_to_job(text, job_description)
                rows.append({
                    "Candidate": resume.name,
                    "Match score": result["match_score"],
                    "Semantic similarity": result["semantic_similarity"],
                    "Skill coverage": result["skill_coverage"]
                })
                details.append((resume.name, result))
            except Exception as exc:
                st.warning(f"{resume.name}: {exc}")
            progress.progress((i + 1) / len(resumes))

        if rows:
            ranking = pd.DataFrame(rows).sort_values("Match score", ascending=False).reset_index(drop=True)
            ranking.index = ranking.index + 1
            st.markdown("### Ranked shortlist")
            st.dataframe(ranking, use_container_width=True)
            st.download_button(
                "Download shortlist as CSV",
                ranking.to_csv(index_label="Rank").encode("utf-8"),
                file_name="aivora_candidate_shortlist.csv",
                mime="text/csv"
            )
            st.markdown("### Explainable candidate results")
            by_name = {name: result for name, result in details}
            for rank, row in ranking.iterrows():
                name = row["Candidate"]
                result = by_name[name]
                with st.expander(f"#{rank} — {name} — {result['match_score']:.1f}%"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Overall prototype score", f"{result['match_score']:.1f}%")
                    c2.metric("Semantic similarity", f"{result['semantic_similarity']:.1f}%")
                    c3.metric("Skill coverage", f"{result['skill_coverage']:.1f}%")
                    st.write("**Matched skills**")
                    st.write(", ".join(result["matched_skills"]) or "No listed skills matched.")
                    st.write("**Missing skills**")
                    st.write(", ".join(result["missing_skills"]) or "No missing skills from the detected skill list.")
                    st.write("**Resume skills detected**")
                    st.write(", ".join(result["resume_skills"]) or "None detected")
        else:
            st.error("No resumes could be analyzed. Check the file formats and contents.")

else:
    st.markdown("### Candidate workspace")
    resume = st.file_uploader("Upload your resume (PDF, DOCX or TXT)", type=["pdf", "docx", "txt"])
    if st.button("Generate my skill-gap report", type="primary", disabled=not (job_description.strip() and resume)):
        try:
            resume_text = extract_text(resume)
            if not resume_text.strip():
                st.error("No readable text found. If this is a scanned PDF, run OCR first.")
            else:
                result = match_resume_to_job(resume_text, job_description)
                c1, c2, c3 = st.columns(3)
                c1.metric("Overall prototype score", f"{result['match_score']:.1f}%")
                c2.metric("Semantic similarity", f"{result['semantic_similarity']:.1f}%")
                c3.metric("Skill coverage", f"{result['skill_coverage']:.1f}%")
                st.progress(result["skill_coverage"] / 100)
                left, right = st.columns(2)
                with left:
                    st.success("Matched skills")
                    st.write(", ".join(result["matched_skills"]) or "No listed skills matched yet.")
                with right:
                    st.warning("Skills to consider developing")
                    st.write(", ".join(result["missing_skills"]) or "No gaps found in the detected skill list.")
                st.info("This report is based on skills detected by the prototype. Review the job description and your resume manually as well.")
        except Exception as exc:
            st.error(f"Could not analyze this resume: {exc}")

st.divider()
st.caption("AIVORA | HACKMINT 2026 | HACM112 — Intelligent Resume-to-Job Matching")
