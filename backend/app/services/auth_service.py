from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
)
from app.models import User
from app.schemas.auth import UserCreate


def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    email = str(user_data.email).lower()

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise ValueError("Email is already registered")

    user = User(
        email=email,
        full_name=user_data.full_name.strip(),
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:

    normalized_email = email.lower()

    user = db.scalar(
        select(User).where(User.email == normalized_email)
    )

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user