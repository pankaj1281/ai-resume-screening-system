from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import ATSReport, Prediction, Resume, User

router = APIRouter(prefix="/admin", tags=["admin"])


def _ensure_admin(user: User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get('/users')
def list_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_admin(current_user)
    users = db.query(User).all()
    return [{"id": u.id, "full_name": u.full_name, "email": u.email} for u in users]


@router.delete('/users/{user_id}')
def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_admin(current_user)
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(target)
    db.commit()
    return {'message': 'User deleted'}


@router.get('/stats')
def stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_admin(current_user)
    return {
        'total_users': db.query(User).count(),
        'total_resumes': db.query(Resume).count(),
        'total_predictions': db.query(Prediction).count(),
        'total_ats_reports': db.query(ATSReport).count(),
    }
