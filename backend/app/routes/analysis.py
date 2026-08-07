import json
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, rate_limit
from ..models import ATSReport, History, Prediction, Resume, User
from ..schemas import ATSRequest, ATSResponse, CompareJobRequest, CompareJobResponse, HistoryItem, PredictRequest, PredictionResponse
from ..services.ats import compute_ats_score
from ..services.job_matcher import compare_resume_with_jd
from ..services.predictor import predictor
from ..services.resume_parser import extract_text, parse_resume

router = APIRouter(tags=["analysis"])


@router.post('/upload')
async def upload_resume(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db), _=Depends(rate_limit)):
    raw = await file.read()
    if len(raw) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail='File size exceeds 10 MB')
    text = extract_text(file, raw)
    parsed = parse_resume(text)

    resume = Resume(user_id=user.id, filename=file.filename, content=text)
    db.add(resume)
    db.add(History(user_id=user.id, action='upload', details=json.dumps({'filename': file.filename})))
    db.commit()
    db.refresh(resume)

    return {'resume_id': resume.id, 'parsed_resume': parsed.model_dump()}


@router.post('/predict', response_model=PredictionResponse)
def predict(payload: PredictRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db), _=Depends(rate_limit)):
    result = predictor.predict(payload.text)
    resume = Resume(user_id=user.id, filename='manual_input.txt', content=payload.text)
    db.add(resume)
    db.commit()
    db.refresh(resume)

    db.add(Prediction(resume_id=resume.id, predicted_category=result['category'], confidence=result['confidence']))
    db.add(History(user_id=user.id, action='predict', details=json.dumps(result)))
    db.commit()
    return result


@router.post('/ats-score', response_model=ATSResponse)
def ats_score(payload: ATSRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db), _=Depends(rate_limit)):
    result = compute_ats_score(payload.text, payload.job_description)
    resume = Resume(user_id=user.id, filename='ats_input.txt', content=payload.text)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    db.add(ATSReport(resume_id=resume.id, score=result['score'], deductions=json.dumps(result['deductions'])))
    db.add(History(user_id=user.id, action='ats-score', details=json.dumps({'score': result['score']})))
    db.commit()
    return result


@router.post('/compare-job', response_model=CompareJobResponse)
def compare_job(payload: CompareJobRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db), _=Depends(rate_limit)):
    result = compare_resume_with_jd(payload.resume_text, payload.job_description)
    db.add(History(user_id=user.id, action='compare-job', details=json.dumps({'similarity': result['similarity_score']})))
    db.commit()
    return result


@router.get('/history', response_model=list[HistoryItem])
def history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(History).filter(History.user_id == user.id).order_by(History.created_at.desc()).all()
    output = []
    for i in items:
        metadata = json.loads(i.details) if i.details else None
        output.append(HistoryItem(action=i.action, metadata=metadata, created_at=i.created_at))
    return output


@router.get('/profile')
def profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume_count = db.query(Resume).filter(Resume.user_id == user.id).count()
    return {
        'id': user.id,
        'full_name': user.full_name,
        'email': user.email,
        'is_admin': user.is_admin,
        'resumes_uploaded': resume_count,
    }
