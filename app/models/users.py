from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(150), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    username: str = Field(..., min_length=3, max_length=150)
    password: str = Field(..., min_length=6)
    email: Optional[str]

class UserOut(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(128), nullable=False, index=True)
    issued_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)
    revoked = Column(Boolean, default=False)
    client_id = Column(String(200), nullable=True)

    user = relationship("User", back_populates="refresh_tokens")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: str
    refresh_expires_in: int
    # optional basic user info to return on login
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    user_id: int

class LoginRequest(BaseModel):
    username: str
    password: str
    client_id: Optional[str] = None

class RefreshRequest(BaseModel):
    refresh_token: str
    client_id: Optional[str] = None