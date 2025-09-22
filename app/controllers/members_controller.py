from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.members_service import fetch_members_for_user
from app.models.members import Member
from typing import List
from fastapi import status
from app.utils.auth_util import get_current_user_id

router = APIRouter(prefix="/members", tags=["members"])

@router.get("", response_model=List[dict])
def get_members_for_user(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    members = fetch_members_for_user(db, user_id)
    # Only return member_id, relationship, full_name
    return [
        {
            "member_id": m.member_id,
            "relationship": m.relationship,
            "full_name": m.full_name
        } for m in members
    ]
