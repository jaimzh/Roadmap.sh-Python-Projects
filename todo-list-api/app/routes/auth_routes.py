
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import schemas
from app.services import user_service
from app.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(registration_data: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = user_service.get_user_by_email(db, email=registration_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )
    new_user = user_service.create_user(db=db, user_data=registration_data )
    return new_user


        
        
@router.post("/login")
def login(
    # Use Depends(OAuth2PasswordRequestForm) instead of your Pydantic schema
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Using form_data.username (Swagger automatically maps the email input here)
    user = user_service.get_user_by_email(db, email=form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/login", response_model=schemas.Token)
# def login_user(login_data:schemas.UserLogin, db: Session = Depends(get_db) ):
#     #Verifies user credentials and issues a secure JWT access token.
#     user = user_service.get_user_by_email(db, email=login_data.email)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password."
#         )
        
#     if not verify_password(login_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password."
#         )
        
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}