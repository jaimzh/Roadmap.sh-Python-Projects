from sqlalchemy.orm import Session
from app.models.db import User
from app.models import schemas
from app.utils.security import hash_password


def get_user_by_email(db: Session, email: str):
  
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: schemas.UserRegister):
    
    # 1. Scramble the raw text password
    hashed_pwd = hash_password(user_data.password)
    
    # Map the schema data to our SQLAlchemy Database Model
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pwd
        # is_active will automatically default to True based on our model setup
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user