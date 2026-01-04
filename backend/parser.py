# backend/parser.py

import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text.strip()

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join(p.text for p in doc.paragraphs).strip()

def extract_resume_text(file):
    try:
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            return None

        if not text or len(text) < 50:
            return None

        return text
    except Exception:
        return None
