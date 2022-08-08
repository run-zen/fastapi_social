from datetime import datetime
from pydantic import BaseModel, EmailStr, conint, validator
from typing import Optional, List


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


class ContactSchema(BaseModel):
    id: int
    phone_number: str
    name: str
    password: str
    created_at: datetime


class ChatSchema(BaseModel):
    id: int
    participants: List[str]
    removed_participants: List[str]
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


class ContactOut(BaseModel):
    phone_number: str
    name: Optional[str]

    @validator('phone_number')
    def receiver_validate(cls, v: str):
        if len(v) == 10:
            return v
        raise ValueError('Please enter correct receiver phone number')


class ContactCreate(ContactOut):
    password: str


class ContactLogin(BaseModel):
    phone_number: str
    password: str

    @validator('phone_number')
    def receiver_validate(cls, v: str):
        if len(v) == 10:
            return v
        raise ValueError('Please enter correct receiver phone number')


class CreateChat(BaseModel):
    participant: str


class ChatOut(BaseModel):
    participants: List[str]


class SendMessage(BaseModel):
    receiver: str
    message: str

    @validator('receiver')
    def receiver_validate(cls, v: str):
        if len(v) == 10:
            return v
        raise ValueError('Please enter correct receiver phone number')


class GetMessage(BaseModel):
    chat_id: int


class GetMessageByID(BaseModel):
    id: int


class CreateMessage(BaseModel):
    chat_id: int
    receiver_id: int
    sender_id: int
    text_message: str


class UpdateTime(BaseModel):
    id: int

