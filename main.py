# main.py
import streamlit as st
import json

from resume_parser import read_resume
from jd_parser import extract_skills_from_jd, extract_years_requirement
from scoring import compute_match_score
from generator import generate_tailored_bullets, generate_cover_letter

st.set_page_config(page_title="GenAI Job Assistant", layout="wide")
st.title("GenAI Job Application Assistant using Gemini")

with st.sidebar:
    st.header("Settings")
    name = st.text_input("Your name", "Candidate Name")
    job_title = st.text_input("Target job title", "Software Engineer")
    company = st.text_input("Company", "Company Name")
    num_bullets = st.slider("Number of bullets", 2, 6, 4)

st.header("1) Upload Resume (PDF or TXT)")
resume_file = st.file_uploader("Upload file", type=["pdf", "txt"])

st.header("2) Paste Job Description")
jd_text = st.text_area("Job description", height=280)

if st.button("Analyze & Generate"):

    if not resume_file:
        st.error("Upload resume first.")
        st.stop()

    if not jd_text.strip():
        st.error("Paste the job description.")
        st.stop()

    resume_text = read_resume(resume_file)
    if not resume_text:
        st.error("Could not extract resume text.")
        st.stop()

    with st.spinner("Extracting skills..."):
        jd_skills = extract_skills_from_jd(jd_text)
        resume_skills = extract_skills_from_jd(resume_text)   # use same extractor for resume


    st.subheader("JD Skills")
    st.json(jd_skills)

    st.subheader("Resume Skills")
    st.json(resume_skills)

    score_pct, details = compute_match_score(jd_text, resume_text, jd_skills)


    # # === Enhanced Match Score UI ===
    # st.write("### Match Score")
    # st.progress(score_pct / 100)

    # # Badge color logic
    # if score_pct < 40:
    #     color = "#D9534F"  # red
    #     label = "Low Match"
    # elif score_pct < 70:
    #     color = "#F0AD4E"  # orange
    #     label = "Medium Match"
    # else:
    #     color = "#5CB85C"  # green
    #     label = "High Match"

    # # Badge UI Box
    # st.markdown(
    #     f"""
    #     <div style='padding:10px;border-radius:8px;background-color:{color};
    #                 color:white;text-align:center;font-size:18px;margin-top:10px;'>
    #         {label}: {score_pct}%
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

    # # Feedback messages
    # if score_pct == 0:
    #     st.warning("⚠️ No matching skills found — try adding a clearer job description.")
    # elif score_pct < 40:
    #     st.error("❌ Low match. Your resume needs stronger alignment with the JD.")
    # elif score_pct < 70:
    #     st.info("🙂 Medium match — improving keywords and bullets will help.")
    # else:
    #     st.success("🔥 High match! Your resume strongly aligns with this job.")

    # # Show scoring details
    # st.json(details)

    # === ATS Score Card UI ===

    st.markdown("## Match Score Overview")

    # Progress Bar
    st.progress(score_pct / 100)

    # Badge Classification
    if score_pct < 40:
        color = "#D9534F"  # red
        label = "Low Match"
    elif score_pct < 70:
        color = "#F0AD4E"  # orange
        label = "Medium Match"
    else:
        color = "#5CB85C"  # green
        label = "High Match"

    # Score Card Box
    st.markdown(
        f"""
        <div style='padding:18px;border-radius:10px;background-color:{color};
                    color:white;text-align:center;font-size:20px;font-weight:bold;margin-top:10px;'>
            {label}: {score_pct}%
        </div>
        """,
        unsafe_allow_html=True
    )

    # Summary Row
    # st.markdown(
    #     f"""
    #     <div style='margin-top:15px;padding:15px;border-radius:10px;background:#f7f7f7;
    #                 border:1px solid #ddd;'>
    #         <h4 style='margin:0;'>Match Details</h4>
    #         <ul>
    #             <li><b>Semantic Similarity:</b> {details['semantic_score']}</li>
    #             <li><b>Keyword Match Score:</b> {details['keyword_score']}</li>
    #             <li><b>Matched Skills:</b> {", ".join(details['matched_skills']) if details['matched_skills'] else "None"}</li>
    #         </ul>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

    # Match Details Card (dark-mode friendly)
    st.markdown(
        f"""
        <div style="
            margin-top:15px;
            padding:15px;
            border-radius:10px;
            background:rgba(255, 255, 255, 0.05);
            border:1px solid rgba(255, 255, 255, 0.1);
            color:#f2f2f2;
            ">
            <h4 style='margin:0 0 10px 0; color:#ffffff;'>Match Details</h4>
            <ul style='margin:0; padding-left:20px;'>
                <li><b>Semantic Similarity:</b> {details['semantic_score']}</li>
                <li><b>Keyword Match Score:</b> {details['keyword_score']}</li>
                <li><b>Matched Skills:</b> {", ".join(details['matched_skills']) if details['matched_skills'] else "None"}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )



    # Feedback Messages
    if score_pct == 0:
        st.warning("⚠️ No matching skills found — try adding a clearer job description.")
    elif score_pct < 40:
        st.error("❌ Low alignment — consider adding more relevant skills to your resume.")
    elif score_pct < 70:
        st.info("🙂 Medium alignment — your resume matches partially. Some improvements will help.")
    else:
        st.success("🔥 Excellent alignment! Your resume is highly suitable for this role.")

    # # Still show raw JSON below for debugging if needed
    # with st.expander("View Raw Match Details"):
    #     st.json(details)



    with st.spinner("Generating resume bullets..."):
        bullets = generate_tailored_bullets(jd_skills, resume_text, num_bullets)

    st.subheader("Tailored Bullets")
    for b in bullets:
        st.markdown(f"- {b}")

    with st.spinner("Generating cover letter..."):
        cover_letter = generate_cover_letter(name, job_title, company, resume_text, bullets, jd_text)

    st.subheader("Cover Letter")
    st.text_area("Generated Cover Letter", cover_letter, height=300)

    st.download_button("Download Cover Letter", cover_letter, file_name="cover_letter.txt")
