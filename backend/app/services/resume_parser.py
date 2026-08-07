import io
import re
from pathlib import Path

import docx
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader

from ..schemas import ParsedResume

SKILL_SET = {
    "python", "java", "c++", "sql", "tensorflow", "pytorch", "fastapi", "django",
    "react", "node", "docker", "kubernetes", "aws", "azure", "git", "machine learning",
    "nlp", "xgboost", "lightgbm", "scikit-learn", "javascript", "typescript", "mongodb"
}


def _extract_text_from_pdf(raw: bytes) -> str:
    reader = PdfReader(io.BytesIO(raw))
    return "
".join(page.extract_text() or "" for page in reader.pages)


def _extract_text_from_docx(raw: bytes) -> str:
    doc = docx.Document(io.BytesIO(raw))
    return "
".join(p.text for p in doc.paragraphs)


def extract_text(upload: UploadFile, raw: bytes) -> str:
    suffix = Path(upload.filename).suffix.lower()
    if suffix == ".pdf":
        return _extract_text_from_pdf(raw)
    if suffix == ".docx":
        return _extract_text_from_docx(raw)
    if suffix == ".txt":
        return raw.decode("utf-8", errors="ignore")
    raise HTTPException(status_code=400, detail="Unsupported file type")


def parse_resume(text: str) -> ParsedResume:
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.search(r"(?:\+?\d{1,3}[\s-]?)?(?:\d[\s-]?){10,}", text)
    linkedin = re.search(r"https?://(?:www\.)?linkedin\.com/[^\s]+", text)
    github = re.search(r"https?://(?:www\.)?github\.com/[^\s]+", text)
    portfolio = re.search(r"https?://[^\s]+", text)

    lower = text.lower()
    skills = sorted({skill for skill in SKILL_SET if skill in lower})

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    full_name = lines[0] if lines else None

    def section(prefixes: tuple[str, ...]) -> list[str]:
        return [line for line in lines if line.lower().startswith(prefixes)]

    return ParsedResume(
        full_name=full_name,
        email=email.group(0) if email else None,
        phone=phone.group(0) if phone else None,
        linkedin=linkedin.group(0) if linkedin else None,
        github=github.group(0) if github else None,
        portfolio=portfolio.group(0) if portfolio else None,
        skills=skills,
        education=section(("education", "b.tech", "bachelor", "master", "university")),
        experience=section(("experience", "worked", "software engineer", "intern")),
        projects=section(("project",)),
        certifications=section(("certification", "certificate")),
        languages=section(("language",)),
        internships=section(("internship",)),
        achievements=section(("achievement", "award")),
    )
