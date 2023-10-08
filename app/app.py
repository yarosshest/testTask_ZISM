from typing import Annotated

import uvicorn as uvicorn
from fastapi import Cookie, FastAPI, Response, Header, Request, Form
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from database.async_db import AsyncHandler as DB
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from database.db_init import db_init
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from pathlib import Path

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="/app/app/templates/")
app = FastAPI()

app.mount("/app/app/static", StaticFiles(directory="/app/app/static"), name="static")


class Message(BaseModel):
    message: str


@app.get("/addPost", response_class=HTMLResponse)
async def add_post_get(request: Request):
    return templates.TemplateResponse("add_post.html", {
        "request": request,
    })


@app.post("/addPost")
async def add_post_post(autor: Annotated[str, Form()], topic: Annotated[str, Form()],
                        body: Annotated[str, Form()]):
    await DB.add_post(autor, topic, body)
    return RedirectResponse("/", status_code=303)


@app.post("/dellPost/{post_id}",
          responses={
              202: {"model": Message, "description": "ok"},
              404: {"model": Message, "description": "Not found"}
          })
async def dell_post(post_id: int):
    res = await DB.dell_post(post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@app.get("/editPost/{post_id}",
         responses={
             404: {"model": Message, "description": "Not found"}},
         response_class=HTMLResponse)
async def edit_post_get(request: Request, post_id: int):
    post = await DB.get_post(post_id)
    if post is not None:
        return templates.TemplateResponse("edit_post.html", {
            "request": request,
            "post": post
        })
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@app.post("/editPost/{post_id}")
async def edit_post_post(post_id: int, autor: Annotated[str, Form()], topic: Annotated[str, Form()],
                         body: Annotated[str, Form()]):
    res = await DB.edit_post(post_id, autor, topic, body)
    if res:
        return RedirectResponse("/", status_code=303)
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    posts = await DB.get_posts()
    posts = list(posts)
    return templates.TemplateResponse("main_page.html", {
        "request": request,
        "posts": posts
    })


@app.post("/like/{post_id}",
          responses={
              202: {"model": Message, "description": "ok"},
              404: {"model": Message, "description": "Not found"}}
          )
async def like_post(post_id: int):
    res = await DB.like_post(post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@app.post("/dislike/{post_id}",
          responses={
              202: {"model": Message, "description": "ok"},
              404: {"model": Message, "description": "Not found"}}
          )
async def dislike_post(post_id: int):
    res = await DB.dislike_post(post_id)
    if res:
        return JSONResponse(status_code=202, content={"message": "ok"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


def api_main():
    db_init()
    uvicorn.run(app, host="0.0.0.0", port=8031)
    # uvicorn.run('app.app.main:app', host="0.0.0.0", port=8031, workers=4)


if __name__ == "__main__":
    api_main()
