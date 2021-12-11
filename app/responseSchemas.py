from datetime import datetime
from typing import Optional, List
from app.schemas import PostBase,UserOut
from pydantic import BaseModel


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class User(UserOut):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ResponseBase(BaseModel):
    message: Optional[str]


class MultiplePost(ResponseBase):
    data: List[Post]


class SinglePost(ResponseBase):
    data: Post


class SingleUser(ResponseBase):
    data: User

