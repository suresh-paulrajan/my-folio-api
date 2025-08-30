from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.config.database import Base
from datetime import datetime

class Member(Base):
    __tablename__ = "members"
    member_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(150), nullable=False)
    relationship = Column(Enum('SELF','SPOUSE','SON','DAUGHTER','FATHER','MOTHER','OTHER'), default='SELF')
    dob = Column(Date, nullable=True)
    email = Column(String(150), nullable=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# Pydantic Schemas
from pydantic import BaseModel, EmailStr
from typing import Optional

class MemberBase(BaseModel):
    full_name: str
    relationship: str
    dob: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]

class MemberCreate(MemberBase):
    user_id: int

class MemberOut(MemberBase):
    member_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
