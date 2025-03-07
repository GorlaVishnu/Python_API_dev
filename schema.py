from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class PostCreate(PostBase):
    title : str
    content : str


class Post(BaseModel):
    id : int
    title : str
    content : str
    created_at : datetime
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str
class Token(BaseModel):
    access_token : str
    token_type : str
class TokenData(BaseModel):
    id : Optional[int] = None

