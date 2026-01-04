# AI Resume–Job Matching System (ATS)

An **AI-powered Applicant Tracking System (ATS)** built using **Python, NLP, and Streamlit** that automatically matches multiple resumes against a job description and ranks candidates using **multi-factor ATS scoring**.

This project simulates how **real-world ATS platforms** shortlist candidates based on skills, experience, education, and text relevance.

---

## Features

- Upload **multiple resumes** (TXT / PDF / DOCX)
- Paste **job description**
- Select **Experience & Education requirements** via dropdowns
- **Multi-factor ATS scoring**:
  - Text relevance (TF-IDF + cosine similarity)
  - Skill coverage
  - Experience match
  - Education match
- Automatically ranks candidates and shortlists **Top-K (up to 50)**
- Line chart visualization (best candidate shown on the right)
- Paginated resume upload preview (10 resumes per page)
- Download **best-fit resumes as ZIP**
- Single-screen, recruiter-friendly dashboard (no scrolling)

---

## ATS Scoring Logic

Final ATS Score is calculated using weighted components:

| Component | Weight |
Text Match | 40% |
Skill Coverage | 30% |
Experience Match | 20% |
Education Match | 10% |

This ensures **realistic and conservative scoring**.

---

## Experience Extraction Strategy

Experience is extracted using a **hybrid approach**:

1. Explicit numeric patterns (e.g., `5+ years`)
2. Date ranges (e.g., `2019–2023`, `2020–Present`)
3. Heuristic fallback based on role keywords (Senior, Lead, Architect)

---

## Tech Stack

- Python
- Streamlit
- scikit-learn
- NLTK
- PyMuPDF (fitz)
- python-docx
- Pandas

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Author

**Neel Bhanvadiya**
