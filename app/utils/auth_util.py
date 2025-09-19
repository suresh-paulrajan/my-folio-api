import os
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.users import User

JWT_SECRET = os.getenv("JWT_SECRET", "replace-with-strong-secret")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRES_SECONDS", "900"))  # 15 min
REFRESH_TOKEN_EXPIRES_SECONDS = int(os.getenv("REFRESH_TOKEN_EXPIRES_SECONDS", str(14*24*3600)))  # 14 days

security = HTTPBearer()

def hash_refresh_token(token: str) -> str:
    # return hex SHA-256
    return hashlib.sha256(token.encode('utf-8')).hexdigest()

def create_refresh_token_plain() -> str:
    # use a strong random opaque token (not predictable)
    return secrets.token_urlsafe(64)

def create_access_token(subject: str, extra: dict = None) -> tuple[str, int]:
    # Use timezone-aware UTC time
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=ACCESS_TOKEN_EXPIRES_SECONDS)
    
    payload = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp())
    }
    if extra:
        payload.update(extra)
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token, ACCESS_TOKEN_EXPIRES_SECONDS

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> int:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    # Optional: verify user still exists and is active
    user = db.query(User).get(user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or not found user")
    return user_id