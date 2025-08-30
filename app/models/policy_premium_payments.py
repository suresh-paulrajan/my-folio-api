from sqlalchemy import Column, Integer, Date, DECIMAL, Enum, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.config.database import Base
from datetime import datetime

class PolicyPremiumPayment(Base):
    __tablename__ = "policy_premium_payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("insurance_policies.policy_id", ondelete="CASCADE"), nullable=False)
    paid_date = Column(Date, nullable=False)
    amount = Column(DECIMAL(12,2), nullable=False)
    method = Column(Enum('ONLINE','NETBANKING','CREDIT_CARD','DEBIT_CARD','UPI','CASH','CHEQUE','OTHER'), default='OTHER')
    reference_no = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

# Pydantic Schemas
from pydantic import BaseModel
from typing import Optional

class PolicyPremiumPaymentBase(BaseModel):
    paid_date: str
    amount: float
    method: str
    reference_no: Optional[str]
    notes: Optional[str]

class PolicyPremiumPaymentCreate(PolicyPremiumPaymentBase):
    policy_id: int

class PolicyPremiumPaymentOut(PolicyPremiumPaymentBase):
    payment_id: int
    policy_id: int
    created_at: datetime

    class Config:
        orm_mode = True
