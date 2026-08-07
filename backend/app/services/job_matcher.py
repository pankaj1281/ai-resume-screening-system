from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .nlp import extract_keywords


def compare_resume_with_jd(resume_text: str, job_description: str):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0])

    resume_kw = extract_keywords(resume_text)
    jd_kw = extract_keywords(job_description)
    matched = sorted(resume_kw & jd_kw)
    missing = sorted(jd_kw - resume_kw)

    suggestions = []
    if missing:
        suggestions.append("Add missing JD skills/keywords in relevant projects and experience bullet points")
    if similarity < 0.45:
        suggestions.append("Rewrite summary to align with required responsibilities")
    if "achievement" not in resume_text.lower():
        suggestions.append("Include measurable achievements with numbers and action verbs")

    return {
        "similarity_score": round(similarity * 100, 2),
        "matched_keywords": matched[:30],
        "missing_keywords": missing[:30],
        "suggestions": suggestions,
    }
