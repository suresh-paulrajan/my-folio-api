from sqlalchemy import Column, Integer, ForeignKey, Enum, Boolean, String, Text, TIMESTAMP, DateTime
from sqlalchemy.sql import func
from app.config.database import Base
from datetime import datetime

class ReminderTask(Base):
    __tablename__ = "reminder_tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    policy_id = Column(Integer, ForeignKey("insurance_policies.policy_id", ondelete="CASCADE"), nullable=True)
    channel = Column(Enum('EMAIL'), default='EMAIL')
    task_kind = Column(Enum('POLICY_PREMIUM','POLICY_MATURITY','CUSTOM'), nullable=False)
    lead_days = Column(Integer, default=7)
    interval_months = Column(Integer, nullable=True)
    next_run_at = Column(DateTime, nullable=False)
    last_run_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)
    subject_template = Column(String(255), nullable=True)
    body_template = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# Pydantic Schemas
from pydantic import BaseModel
from typing import Optional

class ReminderTaskBase(BaseModel):
    policy_id: Optional[int]
    channel: str
    task_kind: str
    lead_days: Optional[int]
    interval_months: Optional[int]
    next_run_at: str
    last_run_at: Optional[str]
    active: Optional[bool]
    subject_template: Optional[str]
    body_template: Optional[str]

class ReminderTaskCreate(ReminderTaskBase):
    user_id: int

class ReminderTaskOut(ReminderTaskBase):
    task_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
