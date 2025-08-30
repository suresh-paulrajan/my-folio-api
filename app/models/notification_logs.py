from sqlalchemy import Column, Integer, ForeignKey, String, Text, TIMESTAMP, Enum
from sqlalchemy.sql import func
from app.config.database import Base
from datetime import datetime

class NotificationLog(Base):
    __tablename__ = "notification_logs"
    log_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("reminder_tasks.task_id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    policy_id = Column(Integer, ForeignKey("insurance_policies.policy_id", ondelete="SET NULL"), nullable=True)
    sent_to = Column(String(150), nullable=False)
    subject = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)
    sent_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(Enum('SENT','FAILED'), default='SENT')
    error = Column(Text, nullable=True)

# Pydantic Schemas
from pydantic import BaseModel
from typing import Optional

class NotificationLogBase(BaseModel):
    task_id: Optional[int]
    user_id: int
    policy_id: Optional[int]
    sent_to: str
    subject: Optional[str]
    body: Optional[str]
    status: Optional[str]
    error: Optional[str]

class NotificationLogCreate(NotificationLogBase):
    pass

class NotificationLogOut(NotificationLogBase):
    log_id: int
    sent_at: datetime

    class Config:
        orm_mode = True
