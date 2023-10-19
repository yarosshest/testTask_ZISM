from __future__ import annotations
import datetime
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Any, List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'User_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    posts: Mapped[List["Post"]] = relationship(back_populates="user")


class Post(Base):
    __tablename__ = 'Post_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    likes: Mapped[int]
    autor: Mapped[str]
    topic: Mapped[str]
    body: Mapped[str]
    time_created: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("User_table.id"))
    user: Mapped["User"] = relationship(back_populates="posts")

    def __init__(self, autor, topic, body, user_id, **kw: Any):
        super().__init__(**kw)
        self.autor = autor
        self.topic = topic
        self.body = body
        self.likes = 0
        self.user_id = user_id

