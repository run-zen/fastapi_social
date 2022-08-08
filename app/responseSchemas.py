from datetime import datetime
from typing import Optional, List
from app.schemas import PostBase, UserOut, ContactOut, CreateChat, ChatOut
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


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class ResponseBase(BaseModel):
    statuscode: Optional[int] = 200
    message: Optional[str]


class MultiplePost(ResponseBase):
    foundResults: Optional[int]
    numResults: Optional[int]
    data: List[PostOut]


class SinglePost(ResponseBase):
    data: PostOut


class SingleUser(ResponseBase):
    data: User


class Token(BaseModel):
    access_token: str
    token_type: str


class Contact(ContactOut):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class SingleContact(ResponseBase):
    data: Contact
    access_token: Optional[str]
    token_type: Optional[str]


class Chat(ChatOut):
    id: int

    class Config:
        orm_mode = True


class SingleChat(ResponseBase):
    data: Chat


class ContactLogin(BaseModel):
    access_token: str
    token_type: str
    user: Contact
