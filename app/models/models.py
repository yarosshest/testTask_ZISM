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


def from_db_post(post: DbPost):
    return Post(
        id=post.id,
        likes=post.likes,
        autor=post.autor,
        topic=post.topic,
        body=post.body
    )
