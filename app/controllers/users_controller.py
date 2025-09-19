from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services import users_service
from typing import List
from app.models.users import User, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/count", response_model=int)
def read_users_count(db: Session = Depends(get_db)):
    return users_service.get_users_count(db)

@router.get("/list", response_model=List[UserOut])
def fetch_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users    