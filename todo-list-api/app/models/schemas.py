from pydantic import BaseModel, EmailStr
from typing import Optional

# TODO SCHEMA 
class TodoRequest(BaseModel):
    title: str
    description: Optional[str] = None
    
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool
    user_id: int

    class Config: 
        from_attributes = True #this allows pydantic to read raw sqlalchemy object directly
        #because we are getting a response, we are converting raw sql to a claen json, it is just used for translation
        
 
# AUTH SCHEMAS
#front
class UserRegister(BaseModel): 
    name: str
    email: EmailStr
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
#after successful login we attatch token 
class Token(BaseModel): 
    access_token: str  #the expiration date is baked into the access token btw 
    token_type: str ="bearer" # Default token type for OAuth2/JWT #
    
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
          from_attributes = True    