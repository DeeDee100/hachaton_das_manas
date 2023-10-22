from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "user_db"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    age =  Column(Integer, nullable=True)
    raca =  Column(String, nullable=True)
    uf =  Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_onupdate=func.now())

    posts =  relationship(
        "Post",
        back_populates="user",
        uselist=True,
    )
    
    replies =  relationship(
        "Reply",
        back_populates="user",
        uselist=True,
    )


class Post(Base):
    __tablename__ = "post_db"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_db.id"))
    user = relationship("User", back_populates="posts")
    replies = relationship("Reply", uselist=True)

    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_onupdate=func.now())


class Reply(Base):
    __tablename__ = "reply_db"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_db.id"))
    user = relationship("User", back_populates="replies")
    post_id = Column(Integer, ForeignKey("post_db.id"))
    post = relationship("Post", back_populates="replies")
    
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), server_onupdate=func.now())
