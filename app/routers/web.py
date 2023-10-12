from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from database.async_db import AsyncHandler as DB, get_session
from app.models.models import Message

import os

router = APIRouter(
    prefix="/web",
    tags=["web"],
)

templates = Jinja2Templates(directory="/app/app/templates/")


@router.get("/addPost", response_class=HTMLResponse)
async def add_post_get(request: Request):
    return templates.TemplateResponse("add_post.html", {
        "request": request,
    })


@router.post("/addPost")
async def add_post_post(autor: Annotated[str, Form()],
                        topic: Annotated[str, Form()],
                        body: Annotated[str, Form()],
                        session: AsyncSession = Depends(get_session)
                        ):
    await DB.add_post(session, autor, topic, body)
    return RedirectResponse(router.url_path_for("main_page"), status_code=303)


@router.post("/dellPost/{post_id}",
             responses={
                 202: {"model": Message, "description": "ok"},
                 404: {"model": Message, "description": "Not found"}
             })
async def dell_post(post_id: int, session: AsyncSession = Depends(get_session)):
    res = await DB.dell_post(session, post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.get("/editPost/{post_id}",
            responses={
                404: {"model": Message, "description": "Not found"}},
            response_class=HTMLResponse)
async def edit_post_get(request: Request, post_id: int, session: AsyncSession = Depends(get_session)):
    post = await DB.get_post(session, post_id)
    if post is not None:
        return templates.TemplateResponse("edit_post.html", {
            "request": request,
            "post": post
        })
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.post("/editPost/{post_id}")
async def edit_post_post(post_id: int,
                         autor: Annotated[str, Form()],
                         topic: Annotated[str, Form()],
                         body: Annotated[str, Form()],
                         session: AsyncSession = Depends(get_session)
                         ):
    res = await DB.edit_post(session, post_id, autor, topic, body)
    if res:
        return RedirectResponse(router.url_path_for("main_page"), status_code=303)
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request, session: AsyncSession = Depends(get_session)):
    posts = await DB.get_posts(session)
    posts = list(posts)
    return templates.TemplateResponse("main_page.html", {
        "request": request,
        "posts": posts
    })


@router.post("/like/{post_id}",
             responses={
                 202: {"model": Message, "description": "ok"},
                 404: {"model": Message, "description": "Not found"}}
             )
async def like_post(post_id: int, session: AsyncSession = Depends(get_session)):
    res = await DB.like_post(session, post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.post("/dislike/{post_id}",
             responses={
                 202: {"model": Message, "description": "ok"},
                 404: {"model": Message, "description": "Not found"}}
             )
async def dislike_post(post_id: int, session: AsyncSession = Depends(get_session)):
    res = await DB.dislike_post(session, post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})
