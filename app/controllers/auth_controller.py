from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import users_service
from app.models.users import UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=UserOut)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = users_service.authenticate_user(db, user_in.username, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return user

@router.post("/hash-password")
def hash_password(plain_password: str):
    hashed = users_service.get_password_hash(plain_password)
    return {"hashed_password": hashed}