from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db import User
from app.config import settings
#all these stuff above is just for the auth for get current user 
from typing import Optional
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app.config import settings






# pip install "python-jose[cryptography]"
# tell passlib to use byscrypt for hashing passwords

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password=str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    to_encode = data.copy()

    if expires_delta:
        time_to_expire = datetime.now(timezone.utc) + expires_delta
    else:
        time_to_expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Inject the expiration timestamp into the token payload dictionary
    to_encode.update({"exp": time_to_expire})

    # Sign and encrypt everything using our validated .env secret key and algorithm
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Security guard that intercepts requests, decodes the JWT token, 
    and returns the currently authenticated database User object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decode the token using our secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")#get the email from the decoded token 
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # 2. Fetch the actual user from the database using the email from the token
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    # 3. Return the real user object!
    return user