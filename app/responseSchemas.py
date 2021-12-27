from datetime import datetime
from typing import Optional, List
from app.schemas import PostBase, UserOut
from pydantic import BaseModel


class User(UserOut):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: User

    class Config:
        orm_mode = True


class ResponseBase(BaseModel):
    message: Optional[str]


class MultiplePost(ResponseBase):
    foundResults: Optional[int]
    numResults: Optional[int]
    data: List[Post]


class SinglePost(ResponseBase):
    data: Post


class SingleUser(ResponseBase):
    data: User


class Token(BaseModel):
    access_token: str
    token_type: str
