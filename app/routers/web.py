import os
from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.models.models import Message, Token, User
from app.security.security import (authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,
                                   get_password_hash, get_current_user)
from database.async_db import DataBase as Db
from database.async_db import db as db_ins

from pathlib import Path
router = APIRouter(
    prefix="/web",
    tags=["web"],

)

script_dir = Path(__file__).parent.parent.joinpath("templates/")

templates = Jinja2Templates(directory=script_dir)


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
    return RedirectResponse(router.url_path_for("posts_page"), status_code=303)


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
        return RedirectResponse(router.url_path_for("posts_page"), status_code=303)
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.get("/posts", response_class=HTMLResponse)
async def posts_page(request: Request, db: Db = Depends(db_ins)):
    posts = await db.get_posts()
    posts = list(posts)
    return templates.TemplateResponse("main_page.html", {
        "request": request,
        "posts": posts
    })


@router.get("/", response_class=HTMLResponse)
async def login_page_get(request: Request, user: Annotated[User, Depends(get_current_user)]):
    if user is None:
        return templates.TemplateResponse("login_page.html", {
            "request": request
        })

    if not user.disabled:
        return RedirectResponse(router.url_path_for("posts_page"), status_code=303)


@router.post("/", response_class=HTMLResponse,
             responses={
                 401: {"model": Message, "description": "Incorrect username or password"}}
             )
async def login_page_post(request: Request,
                     login: str,
                     password: str,
                     db: Db = Depends(db_ins)
                     ):
    user = await authenticate_user(login, password, db)

    if not user:
        return JSONResponse(status_code=401,
                            content={"message": "Incorrect username or password"},
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    res = RedirectResponse(router.url_path_for("posts_page"),
                            status_code=303,
                            headers={"access_token": access_token, "token_type": "bearer"})

    res.set_cookie(key="access_token", value="access_token")
    res.set_cookie(key="token_type", value="bearer")

    return res


@router.get("/register", response_class=HTMLResponse)
async def register_page_get(request: Request):
    return templates.TemplateResponse("register_page.html", {
        "request": request
    })


@router.post("/register", response_class=HTMLResponse, responses={
    409: {"model": Message, "description": "Already exist"}}
             )
async def register_page_post(login: Annotated[str, Form()],
                        password: Annotated[str, Form()],
                        db: Db = Depends(db_ins)
                        ):
    u = await db.get_user(login)
    if u is None:
        await db.register_user(login, get_password_hash(password))
        return RedirectResponse(router.url_path_for("login_page"), status_code=303)
    else:
        return JSONResponse(status_code=409, content={"message": "Already exist"})


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


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
