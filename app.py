import streamlit as st
from backend import run_matching_multiple_resumes
import zipfile
import io

st.set_page_config(page_title="AI Resume–Job Matching (ATS)", layout="wide")

st.title("📄 AI Resume–Job Matching System (ATS)")
st.caption("Multi-factor ATS scoring with Skills, Experience & Education")

# ===================== MAIN TWO-COLUMN LAYOUT =====================
left_col, right_col = st.columns([2.3, 1])

# ===================== LEFT COLUMN (JOB + RESULTS) =====================
with left_col:
    st.subheader("🧾 Job Description & Results")

    job_text = st.text_area(
        "Job Description",
        height=170,
        placeholder="Hiring a Java Developer with Spring Boot, Microservices, REST APIs..."
    )

    exp_col, edu_col = st.columns(2)

    with exp_col:
        required_experience = st.selectbox(
            "Experience Required",
            ["Any", "0–1", "2–3", "4–6", "7–10", "10+"]
        )

    with edu_col:
        required_education = st.selectbox(
            "Education Required",
            ["Any", "diploma", "bachelors", "masters", "phd"]
        )

    # Placeholder for results (filled after Run)
    results_placeholder = st.empty()

# ===================== RIGHT COLUMN (UPLOAD + RUN) =====================
with right_col:
    st.subheader("📂 Upload & Run")

    uploaded_resumes = st.file_uploader(
        "Upload Resumes (TXT / PDF / DOCX)",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True
    )

    top_k = st.slider(
        "Top Candidates",
        min_value=1,
        max_value=100,
        value=10
    )

    run_btn = st.button("🚀 Run ATS Matching", use_container_width=True)

# ===================== RUN ATS & SHOW RESULTS ON LEFT =====================
if run_btn:
    if not job_text.strip():
        st.warning("Please enter a job description.")
    elif not uploaded_resumes:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Analyzing resumes..."):
            result_df = run_matching_multiple_resumes(
                job_text=job_text,
                uploaded_resumes=uploaded_resumes,
                top_k=top_k,
                required_experience=required_experience,
                required_education=required_education
            )

        with results_placeholder.container():
            st.success("✅ Matching completed")

            tab1, tab2 = st.tabs(["📋 Best-Fit Candidates", "📈 ATS Score Trend"])

            with tab1:
                st.dataframe(
                    result_df[
                        ["Rank", "Resume Name", "Final ATS Score (%)",
                         "Experience (Years)", "Education Level"]
                    ],
                    height=320,
                    use_container_width=True
                )

            with tab2:
                chart_df = (
                    result_df[["Rank", "Final ATS Score (%)"]]
                    .sort_values("Rank", ascending=False)  # Best on right
                    .set_index("Rank")
                )
                st.line_chart(chart_df)

            # ---------------- DOWNLOAD ZIP ----------------
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for _, row in result_df.iterrows():
                    resume_index = int(row["Resume Index"])
                    resume_file = uploaded_resumes[resume_index]
                    zip_file.writestr(resume_file.name, resume_file.getvalue())

            zip_buffer.seek(0)

            st.download_button(
                "⬇️ Download Best-Fit Resumes (ZIP)",
                data=zip_buffer,
                file_name="best_fit_resumes.zip",
                mime="application/zip",
                use_container_width=True
            )