from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import schemas
from app.services import user_service
from app.utils.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


# register creates the user, hashes the password in the service, then returns a token
@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register_user(
    registration_data: schemas.UserRegister, db: Session = Depends(get_db)
):
    existing_user = user_service.get_user_by_email(db, email=registration_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    new_user = user_service.create_user(db=db, user_data=registration_data)
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# JSON login for normal API clients or a frontend app
@router.post("/login", response_model=schemas.Token)
def login(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    user = user_service.get_user_by_email(db, email=login_data.email)

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# form login for Swagger's Authorize button, same auth logic but different input shape
@router.post("/token", response_model=schemas.Token)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = user_service.get_user_by_email(db, email=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
