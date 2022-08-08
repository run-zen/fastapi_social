from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, ARRAY
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False)


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, nullable=False)
    participants = Column(ARRAY(String, dimensions=1), nullable=False, unique=True)
    removed_participants = Column(ARRAY(String, dimensions=1), server_default='{}')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_accessed = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    sender_id = Column(Integer, ForeignKey('contacts.id', ondelete='CASCADE'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('contacts.id', ondelete='CASCADE'), nullable=False)
    text_message = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
