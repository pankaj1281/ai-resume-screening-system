from collections import defaultdict, deque
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .auth import decode_token
from .database import get_db
from .models import User

http_bearer = HTTPBearer(auto_error=False)
_rate_memory: dict[str, deque] = defaultdict(deque)


def rate_limit(request: Request, max_calls: int = 60, window_seconds: int = 60) -> None:
    ip = request.client.host if request.client else "unknown"
    now = datetime.utcnow()
    q = _rate_memory[ip]
    while q and now - q[0] > timedelta(seconds=window_seconds):
        q.popleft()
    if len(q) >= max_calls:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    q.append(now)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization")
    if credentials.scheme.lower() not in {"bearer", "jwt"}:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unsupported authorization scheme")
    token = credentials.credentials
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
