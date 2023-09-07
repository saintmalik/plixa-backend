from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from settings import default_settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expires})
    return jwt.encode(
        to_encode,
        default_settings.JWT_SECRET_KEY,
        algorithm=default_settings.JWT_ALGORITHM,
    )