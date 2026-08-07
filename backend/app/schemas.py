from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)


class ForgotPassword(BaseModel):
    email: EmailStr


class PredictRequest(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    category: str
    confidence: float


class ATSRequest(BaseModel):
    text: str
    job_description: Optional[str] = None


class ATSResponse(BaseModel):
    score: float
    deductions: List[str]
    matched_skills: List[str]
    missing_skills: List[str]


class CompareJobRequest(BaseModel):
    resume_text: str
    job_description: str


class CompareJobResponse(BaseModel):
    similarity_score: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    suggestions: List[str]


class ParsedResume(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    skills: List[str] = []
    education: List[str] = []
    experience: List[str] = []
    projects: List[str] = []
    certifications: List[str] = []
    languages: List[str] = []
    internships: List[str] = []
    achievements: List[str] = []


class HistoryItem(BaseModel):
    action: str
    metadata: Dict[str, Any] | None = None
    created_at: datetime

    class Config:
        from_attributes = True
