from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.users import User

def get_users_count(db: Session) -> int:
    result = db.execute(text("SELECT COUNT(*) FROM users"))
    return result.scalar()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()