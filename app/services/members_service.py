from sqlalchemy.orm import Session
from app.repositories.members_repository import get_members_by_user_id
from app.models.members import Member
from typing import List

def fetch_members_for_user(db: Session, user_id: int) -> List[Member]:
    return get_members_by_user_id(db, user_id)
