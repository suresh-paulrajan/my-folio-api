from sqlalchemy.orm import Session
from sqlalchemy import text

def get_users_count(db: Session) -> int:
    result = db.execute(text("SELECT COUNT(*) FROM users"))
    return result.scalar()