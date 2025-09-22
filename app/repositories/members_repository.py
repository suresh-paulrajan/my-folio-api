from sqlalchemy.orm import Session
from app.models.members import Member
from typing import List


def get_members_by_user_id(db: Session, user_id: int) -> List[Member]:
    return db.query(Member).filter(Member.user_id == user_id).all()
