from typing import Annotated

from fastapi import APIRouter
from fastapi import Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database.async_db import AsyncHandler as DB
from app.models.models import Message, Post, from_db_post

router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
)
router.mount("/app/app/static", StaticFiles(directory="/app/app/static"), name="static")

templates = Jinja2Templates(directory="/app/app/templates/")


@router.post("/addPost",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
             })
async def add_post_post(autor: Annotated[str, Form()], topic: Annotated[str, Form()],
                        body: Annotated[str, Form()]):
    await DB.add_post(autor, topic, body)
    return JSONResponse(status_code=200, content={"message": "Successful Response"})


@router.post("/dellPost/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}
             })
async def dell_post(post_id: int):
    res = await DB.dell_post(post_id)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.post("/editPost/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}
             })
async def edit_post_post(post_id: int, autor: Annotated[str, Form()], topic: Annotated[str, Form()],
                         body: Annotated[str, Form()]):
    res = await DB.edit_post(post_id, autor, topic, body)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.post("/like/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}}
             )
async def like_post(post_id: int):
    res = await DB.like_post(post_id)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.post("/dislike/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}}
             )
async def dislike_post(post_id: int):
    res = await DB.dislike_post(post_id)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.get("/getAllPosts",
            responses={
                200: {"model": list[Post], "description": "Successful Response"}}
            )
async def get_all_posts() -> list[Post]:
    posts = await DB.get_posts()
    posts = list(map(lambda x: from_db_post(x), posts))
    return posts
