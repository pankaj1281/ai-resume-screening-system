from backend.app.services.ats import compute_ats_score
from backend.app.services.job_matcher import compare_resume_with_jd


def test_ats_score_range():
    result = compute_ats_score('python sql experience project education certification achievements')
    assert 0 <= result['score'] <= 100


def test_compare_job_shape():
    result = compare_resume_with_jd('python fastapi sql docker', 'python sql docker aws kubernetes')
    assert 'similarity_score' in result
    assert isinstance(result['matched_keywords'], list)
