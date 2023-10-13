from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.async_db import DataBase as Db
from app.models.models import Message, Post, from_db_post

router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
)


@router.post("/addPost",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
             })
async def add_post_post(autor: Annotated[str, Form()],
                        topic: Annotated[str, Form()],
                        body: Annotated[str, Form()],
                        db: Db = Depends(Db)
                        ):
    await db.add_post(autor, topic, body)
    return JSONResponse(status_code=200, content={"message": "Successful Response"})


@router.post("/dellPost/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}
             })
async def dell_post(post_id: int, db: Db = Depends(Db)):
    res = await db.dell_post(post_id)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.post("/editPost/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}
             })
async def edit_post_post(post_id: int,
                         autor: Annotated[str, Form()],
                         topic: Annotated[str, Form()],
                         body: Annotated[str, Form()],
                         db: Db = Depends(Db)
                         ):
    res = await db.edit_post(post_id, autor, topic, body)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.post("/like/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}}
             )
async def like_post(post_id: int, db: Db = Depends(Db)):
    res = await db.like_post(post_id)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.post("/dislike/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}}
             )
async def dislike_post(post_id: int, db: Db = Depends(Db)):
    res = await db.dislike_post(post_id)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.get("/getAllPosts",
            responses={
                200: {"model": list[Post], "description": "Successful Response"}}
            )
async def get_all_posts(db: Db = Depends(Db)) -> list[Post]:
    posts = await db.get_posts()
    posts = list(map(lambda x: from_db_post(x), posts))
    return posts
