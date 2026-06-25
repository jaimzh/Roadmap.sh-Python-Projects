from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.database import get_db
from app.models.db import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hash the raw password before saving it in the database
def hash_password(password=str) -> str:
    return pwd_context.hash(password)


# compare the login password with the saved hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# creates the JWT; the user email is stored in "sub" and the expiry is baked in
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        time_to_expire = datetime.now(timezone.utc) + expires_delta
    else:
        time_to_expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": time_to_expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# tells Swagger to use /auth/token for the Authorize lock
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# this is the guard for protected routes: decode token, find user, return current user
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user
