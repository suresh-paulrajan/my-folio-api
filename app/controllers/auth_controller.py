from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import auth_service
from app.repositories import auth_repository
from app.models.users import TokenResponse, RefreshTokenResponse, LoginRequest, RefreshRequest, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=dict)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = auth_repository.get_user_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = auth_service.get_password_hash(payload.password)
    user = auth_repository.create_user(db, payload.username, hashed, payload.email)
    return {"id": user.user_id, "username": user.username}

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token_obj = auth_service.login_user(db, user, req.client_id)
    return token_obj

@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh(req: RefreshRequest, db: Session = Depends(get_db)):
    res = auth_service.refresh_access_token(db, req.refresh_token, req.client_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    return res

@router.post("/logout")
def logout(req: RefreshRequest, db: Session = Depends(get_db)):
    auth_service.logout_refresh_token(db, req.refresh_token)
    return {"status": "ok"}