from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.utils.auth_util import create_access_token, create_refresh_token_plain, REFRESH_TOKEN_EXPIRES_SECONDS, hash_refresh_token
from app.repositories.auth_repository import get_user_by_username, get_refresh_token_by_hash, save_refresh_token, revoke_all_user_refresh_tokens, revoke_refresh_token
from app.models.members import Member
from datetime import datetime, timedelta

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_ctx.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user

def login_user(db: Session, user, client_id: str = None):
    access_token, expires_in = create_access_token(subject=user.user_id, extra={"username": user.username})
    refresh_plain = create_refresh_token_plain()
    expires_at = datetime.now() + timedelta(seconds=REFRESH_TOKEN_EXPIRES_SECONDS)
    save_refresh_token(db, user.user_id, refresh_plain, expires_at, client_id)
    # attempt to fetch user's SELF member to provide name/email
    member = db.query(Member).filter(Member.user_id == user.user_id, Member.relationship == 'SELF').first()
    email = None
    name = None
    if member:
        email = getattr(member, 'email', None) or getattr(user, 'email', None)
        name = getattr(member, 'full_name', None)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "refresh_token": refresh_plain,
        "refresh_expires_in": REFRESH_TOKEN_EXPIRES_SECONDS,
        "email": email,
        "name": name,
        "user_id": user.user_id
    }

def refresh_access_token(db: Session, refresh_token_plain: str, client_id: str = None):
    token_hash = hash_refresh_token(refresh_token_plain)
    stored = get_refresh_token_by_hash(db, token_hash)
    if not stored:
        # possible token reuse attack - consider revoking all tokens for the user if suspicious
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    if stored.revoked:
        # token already used/revoked: suspicious => revoke all tokens
        revoke_all_user_refresh_tokens(db, stored.user_id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked (possible replay). All tokens revoked.")
    if stored.expires_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    # rotate: revoke current and issue a new refresh token
    revoke_refresh_token(db, stored)
    # issue new refresh token
    new_refresh_plain = create_refresh_token_plain()
    new_expires_at = datetime.now() + timedelta(seconds=REFRESH_TOKEN_EXPIRES_SECONDS)
    save_refresh_token(db, stored.user_id, new_refresh_plain, new_expires_at, client_id)

    # create new access token
    # fetch user minimal info
    user = stored.user
    access_token, expires_in = create_access_token(subject=user.user_id, extra={"username": user.username})

    # attempt to fetch SELF member for name/email
    member = db.query(Member).filter(Member.user_id == user.user_id, Member.relationship == 'SELF').first()
    email = None
    name = None
    if member:
        email = getattr(member, 'email', None) or getattr(user, 'email', None)
        name = getattr(member, 'full_name', None)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "refresh_token": new_refresh_plain,
        "refresh_expires_in": REFRESH_TOKEN_EXPIRES_SECONDS,
        "email": email,
        "name": name
    }

def logout_refresh_token(db: Session, refresh_token_plain: str):
    token_hash = hash_refresh_token(refresh_token_plain)
    stored = get_refresh_token_by_hash(db, token_hash)
    if stored:
        revoke_refresh_token(db, stored)
    # no error if token absent; idempotent