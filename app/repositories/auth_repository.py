from sqlalchemy.orm import Session
from app.models.users import User, RefreshToken
from app.utils.auth_util import hash_refresh_token
from datetime import datetime, timedelta

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, hashed_password: str, email: str = None):
    user = User(username=username, password_hash=hashed_password, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_refresh_token(db: Session, user_id: int, token_plain: str, expires_at: datetime, client_id: str = None):
    token_hash = hash_refresh_token(token_plain)
    rt = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at, client_id=client_id)
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt

def get_refresh_token_by_hash(db: Session, token_hash: str):
    return db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()

def revoke_refresh_token(db: Session, rt):
    rt.revoked = True
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt

def revoke_all_user_refresh_tokens(db: Session, user_id: int):
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).update({"revoked": True})
    db.commit()