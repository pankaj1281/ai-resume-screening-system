from collections import Counter

from .nlp import extract_keywords


REQUIRED_SKILLS = {
    "data scientist": {"python", "sql", "machine", "learning", "statistics"},
    "machine learning engineer": {"python", "pytorch", "tensorflow", "ml", "deployment"},
    "software engineer": {"python", "java", "sql", "git", "api"},
    "frontend developer": {"react", "javascript", "css", "html", "typescript"},
    "backend developer": {"python", "fastapi", "sql", "docker", "api"},
    "full stack developer": {"react", "node", "sql", "docker", "javascript"},
    "devops engineer": {"docker", "kubernetes", "aws", "ci", "cd"},
}


def compute_ats_score(resume_text: str, job_description: str | None = None):
    resume_kw = extract_keywords(resume_text)
    jd_kw = extract_keywords(job_description or "")
    target_kw = jd_kw or set().union(*REQUIRED_SKILLS.values())

    matched = sorted(resume_kw & target_kw)
    missing = sorted(target_kw - resume_kw)
    match_ratio = (len(matched) / max(len(target_kw), 1))

    sections = Counter({
        "projects": int("project" in resume_text.lower()),
        "experience": int("experience" in resume_text.lower()),
        "education": int("education" in resume_text.lower()),
        "certifications": int("certification" in resume_text.lower()),
        "achievements": int("achievement" in resume_text.lower() or "award" in resume_text.lower()),
    })
    section_bonus = (sum(sections.values()) / 5) * 20
    keyword_points = match_ratio * 80
    score = round(min(100, keyword_points + section_bonus), 2)

    deductions = []
    if len(missing) > 0:
        deductions.append(f"Missing important keywords/skills: {', '.join(missing[:12])}")
    if not sections["projects"]:
        deductions.append("No clear projects section detected")
    if not sections["achievements"]:
        deductions.append("No measurable achievements detected")
    if not sections["certifications"]:
        deductions.append("No certifications listed")

    return {
        "score": score,
        "deductions": deductions,
        "matched_skills": matched[:25],
        "missing_skills": missing[:25],
    }
