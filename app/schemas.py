from datetime import datetime
from pydantic import BaseModel, EmailStr, conint, validator
from typing import Optional


class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    owner_id: int
    created_at: datetime


class UserSchema(BaseModel):
    id: int
    email: str
    password: str
    created_at: datetime


class Vote(BaseModel):
    post_id: int
    dir: int

    @validator('dir')
    def dir_validate(cls, v):
        if v == 1 or v == 0:
            return v
        raise ValueError('direction can ony be 0 or 1')


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None
