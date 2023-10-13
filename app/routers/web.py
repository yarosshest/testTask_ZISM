
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.models.models import Message
from database.async_db import DataBase as Db
from database.async_db import db as db_ins

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
                        db: Db = Depends(db_ins)
                        ):
    await db.add_post(autor, topic, body)
    return RedirectResponse(router.url_path_for("main_page"), status_code=303)


@router.post("/dellPost/{post_id}",
             responses={
                 202: {"model": Message, "description": "ok"},
                 404: {"model": Message, "description": "Not found"}
             })
async def dell_post(post_id: int, db: Db = Depends(db_ins)):
    res = await db.dell_post(post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.get("/editPost/{post_id}",
            responses={
                404: {"model": Message, "description": "Not found"}},
            response_class=HTMLResponse)
async def edit_post_get(request: Request, post_id: int, db: Db = Depends(db_ins)):
    post = await db.get_post(post_id)
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
                         db: Db = Depends(db_ins)
                         ):
    res = await db.edit_post(post_id, autor, topic, body)
    if res:
        return RedirectResponse(router.url_path_for("main_page"), status_code=303)
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request, db: Db = Depends(db_ins)):
    posts = await db.get_posts()
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
async def like_post(post_id: int, db: Db = Depends(db_ins)):
    res = await db.like_post(post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.post("/dislike/{post_id}",
             responses={
                 202: {"model": Message, "description": "ok"},
                 404: {"model": Message, "description": "Not found"}}
             )
async def dislike_post(post_id: int, db: Db = Depends(db_ins)):
    res = await db.dislike_post(post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})
