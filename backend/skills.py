# backend/skills.py

from backend.config import SKILL_SYNONYMS

def normalize_skills(skill_list):
    normalized = set(skill_list)
    for key, values in SKILL_SYNONYMS.items():
        if key in skill_list:
            normalized.update(values)
    return normalized

def calculate_skill_score(resume_text, required_skills):
    resume_text = resume_text.lower()
    matched = 0

    normalized_skills = normalize_skills(required_skills)

    for skill in normalized_skills:
        if skill.lower() in resume_text:
            matched += 1

    if not required_skills:
        return 0

    return matched / len(required_skills)
