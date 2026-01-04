import pandas as pd

from backend.parser import extract_resume_text
from backend.preprocessing import clean_text
from backend.skills import calculate_skill_score
from backend.experience import extract_experience_years
from backend.scoring import text_similarity, calculate_final_score


def run_matching_multiple_resumes(
    job_text,
    uploaded_resumes,
    top_k,
    required_experience,
    required_education
):
    cleaned_job_text = clean_text(job_text)

    results = []

    for idx, file in enumerate(uploaded_resumes):
        resume_text = extract_resume_text(file)
        if resume_text is None:
            continue

        cleaned_resume_text = clean_text(resume_text)

        # --- Core Scores ---
        text_score = text_similarity(cleaned_job_text, cleaned_resume_text)
        skill_score = calculate_skill_score(
            cleaned_resume_text,
            cleaned_job_text.split()
        )
        experience_years = extract_experience_years(resume_text)

        # Simple education logic (can be improved later)
        education_score = 1.0 if required_education == "Any" else (
            1.0 if required_education.lower() in resume_text.lower() else 0.0
        )

        final_score = calculate_final_score(
            text_score,
            skill_score,
            experience_years / 10,  # normalize
            education_score
        )

        results.append({
            "Resume Index": idx,
            "Resume Name": file.name,
            "Final ATS Score (%)": round(final_score * 100, 2),
            "Experience (Years)": experience_years,
            "Education Level": required_education
        })

    df = pd.DataFrame(results)

    if df.empty:
        return df

    df = df.sort_values("Final ATS Score (%)", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1

    return df.head(top_k)
