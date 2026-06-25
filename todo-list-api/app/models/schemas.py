from pydantic import BaseModel, EmailStr
from typing import Optional


# request body for creating or updating a todo
class TodoRequest(BaseModel):
    title: str
    description: Optional[str] = None


# response body when sending a todo back to the client
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool
    user_id: int

    class Config:
        # lets pydantic read SQLAlchemy model objects directly
        from_attributes = True


# request body for creating a new account
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# token response shared by register, JSON login, and Swagger form login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool 

    class Config:
        from_attributes = True


class PaginatedTodoResponse(BaseModel):
    data: list[TodoResponse]
    page: int
    limit: int
    total: int

    class Config:
        # lets the paginated response include SQLAlchemy todo objects
        from_attributes = True
