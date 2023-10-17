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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    h_password: str
    disabled: bool | None = None
