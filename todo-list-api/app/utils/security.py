from typing import Optional

from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings

# tell passlib to use byscrypt for hashing passwords

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password=str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    
    to_encode = data.copy()
    
    if expires_delta:
        time_to_expire = datetime.now(timezone.utc) + expires_delta
    else:
        time_to_expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    # Inject the expiration timestamp into the token payload dictionary
    to_encode.update({"exp": time_to_expire})
    
    # Sign and encrypt everything using our validated .env secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt