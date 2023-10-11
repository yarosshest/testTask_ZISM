from typing import Any

from pydantic import BaseModel

from database.Db_objects import Post as DbPost


class Message(BaseModel):
    message: str


class Post(BaseModel):
    id: int
    likes: int
    autor: str
    topic: str
    body: str

    def __init__(self, post: DbPost, **data: Any):
        super().__init__(**data)
        self.id = post.id
        self.likes = post.likes
        self.autor = post.autor
        self.topic = post.topic
        self.body = post.body

