import pandas as pd
import os
import re
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import fitz  # PDF
from docx import Document  # DOCX


# ---------------- NLTK SAFE SETUP ----------------
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


# ---------------- SKILL ALIASES ----------------
SKILL_ALIASES = {
    "java": ["java", "j2ee"],
    "spring boot": ["spring boot", "springboot"],
    "microservices": ["microservices", "micro service"],
    "rest api": ["rest api", "restful"],
    "sql": ["sql", "mysql", "postgresql", "oracle"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github"],
    "angular": ["angular"],
    "react": ["react", "reactjs"],
    "python": ["python"],
    "machine learning": ["machine learning", "ml"]
}


# ---------------- ATS WEIGHTS ----------------
ATS_WEIGHTS = {
    "text_match": 0.40,
    "skill_coverage": 0.30,
    "experience": 0.20,
    "education": 0.10
}


# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
    return " ".join(tokens)


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    found = set()
    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if alias in text:
                found.add(skill)
                break
    return found


def skill_coverage_percentage(job_skills, resume_skills):
    if not job_skills:
        return 0.0
    return round((len(job_skills & resume_skills) / len(job_skills)) * 100, 2)


# ---------------- EXPERIENCE ----------------

def extract_experience_years(text):
    text = text.lower()

    # ---------- 1️⃣ Explicit numeric experience ----------
    explicit = re.findall(
        r"(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:year|years|yrs)",
        text
    )
    if explicit:
        return int(float(max(explicit)))

    # ---------- 2️⃣ Date range based experience ----------
    year_ranges = re.findall(
        r"(19\d{2}|20\d{2})\s*[-–to]+\s*(present|now|19\d{2}|20\d{2})",
        text
    )

    total_years = 0
    current_year = datetime.now().year

    for start, end in year_ranges:
        start_year = int(start)
        end_year = current_year if end in ["present", "now"] else int(end)
        if end_year >= start_year:
            total_years += end_year - start_year

    if total_years > 0:
        return total_years

    # ---------- 3️⃣ Heuristic fallback ----------
    if "senior" in text:
        return 6
    if "lead" in text or "architect" in text:
        return 8
    if "junior" in text:
        return 1

    return 0

def experience_match_score(candidate_years, required_years):
    if required_years == 0:
        return 1.0
    if candidate_years >= required_years:
        return 1.0
    return round(candidate_years / required_years, 2)


# ---------------- EDUCATION ----------------
def extract_education_level(text):
    text = text.lower()
    if "phd" in text or "doctorate" in text:
        return "phd"
    elif "m.tech" in text or "mtech" in text or "masters" in text or "msc" in text:
        return "masters"
    elif "b.tech" in text or "btech" in text or "b.e" in text or "be" in text or "bachelor" in text:
        return "bachelors"
    elif "diploma" in text:
        return "diploma"
    else:
        return "other"


EDUCATION_SCORE_MAP = {
    "phd": 1.0,
    "masters": 0.9,
    "bachelors": 0.8,
    "diploma": 0.6,
    "other": 0.4
}


def education_match_score(candidate_level, required_level):
    if required_level == "other":
        return 1.0

    c = EDUCATION_SCORE_MAP.get(candidate_level, 0.4)
    r = EDUCATION_SCORE_MAP.get(required_level, 0.4)

    if c >= r:
        return 1.0
    return round(c / r, 2)


# ---------------- FINAL ATS SCORE ----------------
def final_ats_score(text_score, skill_coverage, exp_match, edu_match):
    score = (
        ATS_WEIGHTS["text_match"] * (text_score / 100) +
        ATS_WEIGHTS["skill_coverage"] * (skill_coverage / 100) +
        ATS_WEIGHTS["experience"] * exp_match +
        ATS_WEIGHTS["education"] * edu_match
    )
    return round(score * 100, 2)


# ---------------- FILE READERS ----------------
def extract_text_from_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)


# ---------------- MAIN MATCHING FUNCTION ----------------
def run_matching_multiple_resumes(
    job_text,
    uploaded_resumes,
    top_k=3,
    required_experience="Any",
    required_education="Any"
):
    job_text_cleaned = clean_text(job_text)

    # -------- JOB REQUIREMENTS FROM UI --------
    if required_experience == "Any":
        min_required_exp = 0
    elif required_experience == "10+":
        min_required_exp = 10
    else:
        min_required_exp = int(required_experience.split("–")[0])

    if required_education == "Any":
        min_required_edu = "other"
    else:
        min_required_edu = required_education

    job_skills = extract_skills(job_text_cleaned)

    resume_texts = []
    resume_names = []

    for file in uploaded_resumes:
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file.getvalue())
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            text = file.read().decode("utf-8", errors="ignore")

        resume_texts.append(clean_text(text))
        resume_names.append(file.name)

    # -------- TF-IDF --------
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    vectors = vectorizer.fit_transform(resume_texts + [job_text_cleaned])

    resume_vectors = vectors[:-1]
    job_vector = vectors[-1:]

    similarity_scores = cosine_similarity(resume_vectors, job_vector)

    results = []

    for i, resume_text in enumerate(resume_texts):
        text_score = round(similarity_scores[i][0] * 100, 2)

        resume_skills = extract_skills(resume_text)
        skill_coverage = skill_coverage_percentage(job_skills, resume_skills)
        missing = job_skills - resume_skills

        candidate_exp = extract_experience_years(resume_text)
        exp_match = experience_match_score(candidate_exp, min_required_exp)

        candidate_edu = extract_education_level(resume_text)
        edu_match = education_match_score(candidate_edu, min_required_edu)

        final_score = final_ats_score(
            text_score,
            skill_coverage,
            exp_match,
            edu_match
        )

        results.append({
            "Resume Index": i,
            "Resume Name": resume_names[i],
            "Text Match (%)": text_score,
            "Skill Coverage (%)": skill_coverage,
            "Experience (Years)": candidate_exp,
            "Education Level": candidate_edu,
            "Final ATS Score (%)": final_score,
            "Missing Skills": ", ".join(missing) if missing else "None"
        })

    df = pd.DataFrame(results)

    df = df.sort_values(
        by="Final ATS Score (%)",
        ascending=False
    ).reset_index(drop=True)

    df["Rank"] = df.index + 1
    df["Best Fit"] = df["Rank"].apply(lambda x: "YES" if x <= top_k else "NO")

    best_fit_df = df[df["Best Fit"] == "YES"].reset_index(drop=True)

    os.makedirs("output", exist_ok=True)
    best_fit_df.to_csv("output/results.csv", index=False)

    return best_fit_df