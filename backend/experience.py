# backend/experience.py

import re
from backend.config import MAX_EXPERIENCE_YEARS

def extract_experience_years(text):
    years = []

    patterns = [
        r"(\d+)\+?\s+year",
        r"(\d+)\s+yrs"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            years.append(int(match))

    if years:
        return min(max(years), MAX_EXPERIENCE_YEARS)

    return 0
