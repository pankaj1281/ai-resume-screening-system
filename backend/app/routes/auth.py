from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import create_access_token, hash_password, verify_password
from ..database import get_db
from ..models import User
from ..schemas import ForgotPassword, PasswordChange, Token, UserCreate, UserLogin, UserResponse
from ..deps import get_current_user, rate_limit

router = APIRouter(tags=["auth"])


@router.post('/register', response_model=UserResponse)
def register(payload: UserCreate, db: Session = Depends(get_db), _=Depends(rate_limit)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(full_name=payload.full_name, email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post('/login', response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db), _=Depends(rate_limit)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return Token(access_token=create_access_token(user.email))


@router.post('/change-password')
def change_password(payload: PasswordChange, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(payload.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Old password does not match')
    user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return {'message': 'Password changed successfully'}


@router.post('/forgot-password')
def forgot_password(payload: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return {'message': 'If account exists, reset instructions have been sent'}
    return {'message': 'Use /change-password after login in this demo implementation'}
