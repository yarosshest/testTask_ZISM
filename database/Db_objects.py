from __future__ import annotations
import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Any


class Base(DeclarativeBase):
    pass


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

    def __init__(self, autor, topic, body, **kw: Any):
        super().__init__(**kw)
        self.autor = autor
        self.topic = topic
        self.body = body
        self.likes = 0