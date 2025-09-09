from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, DECIMAL, Boolean, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.config.database import Base
from datetime import datetime, date
# Pydantic Schemas
from pydantic import BaseModel
from typing import Optional

class InsurancePolicy(Base):
    __tablename__ = "insurance_policies"
    policy_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    insured_member_id = Column(Integer, ForeignKey("members.member_id", ondelete="RESTRICT"), nullable=False)
    policy_name = Column(String(255), nullable=False)
    policy_type = Column(Enum('TERM','HEALTH','PERSONAL','AUTO','TOPUP','OTHERS'), nullable=False)
    insurer = Column(String(255), nullable=True)
    policy_number = Column(String(100), nullable=True)
    premium_amount = Column(DECIMAL(12,2), nullable=True)
    premium_frequency = Column(Enum('MONTHLY','QUARTERLY','HALFYEARLY','YEARLY','SINGLE'), nullable=False)
    sum_assured = Column(DECIMAL(15,2), nullable=True)
    start_date = Column(Date, nullable=True)
    next_premium_due_date = Column(Date, nullable=True)
    maturity_date = Column(Date, nullable=True)
    lead_days = Column(Integer, default=7)
    grace_days = Column(Integer, default=15)
    auto_debit = Column(Boolean, default=False)
    policy_status = Column(Enum('ACTIVE','LAPSED','SURRENDERED','MATURED'), default='ACTIVE')
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class InsurancePolicyBase(BaseModel):
    policy_name: str
    policy_type: str
    insurer: Optional[str]
    policy_number: Optional[str]
    premium_amount: Optional[float]
    premium_frequency: str
    sum_assured: Optional[float]
    start_date: Optional[date]
    next_premium_due_date: Optional[date]
    maturity_date: Optional[date]
    lead_days: Optional[int] = 7
    grace_days: Optional[int] = 15
    auto_debit: Optional[bool] = False
    policy_status: Optional[str] = "ACTIVE"
    notes: Optional[str]

class InsurancePolicyUpdate(BaseModel):
    # All fields optional for partial update
    policy_name: Optional[str]
    policy_type: Optional[str]
    insurer: Optional[str]
    policy_number: Optional[str]
    premium_amount: Optional[float]
    premium_frequency: Optional[str]
    sum_assured: Optional[float]
    start_date: Optional[date]
    next_premium_due_date: Optional[date]
    maturity_date: Optional[date]
    lead_days: Optional[int]
    grace_days: Optional[int]
    auto_debit: Optional[bool]
    policy_status: Optional[str]
    notes: Optional[str]

class InsurancePolicyCreate(InsurancePolicyBase):
    user_id: int
    insured_member_id: int

class InsurancePolicyOut(InsurancePolicyBase):
    policy_id: int
    user_id: int
    insured_member_id: int
    insured_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
