# backend/scoring.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.config import (
    TEXT_WEIGHT,
    SKILL_WEIGHT,
    EXPERIENCE_WEIGHT,
    EDUCATION_WEIGHT
)

def text_similarity(job_text, resume_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([job_text, resume_text])
    return cosine_similarity(vectors[0], vectors[1])[0][0]

def calculate_final_score(
    text_score,
    skill_score,
    experience_score,
    education_score
):
    return (
        TEXT_WEIGHT * text_score +
        SKILL_WEIGHT * skill_score +
        EXPERIENCE_WEIGHT * experience_score +
        EDUCATION_WEIGHT * education_score
    )
