from sqlalchemy.orm import Session
from app.repositories import users_repository

def get_users_count(db: Session) -> int:
    return users_repository.get_users_count(db)