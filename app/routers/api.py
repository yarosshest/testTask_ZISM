from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Form
from fastapi.responses import JSONResponse

from app.security.security import get_password_hash, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, get_current_user
from database.Db_objects import User
from database.async_db import DataBase as Db
from app.models.models import Message, Post, from_db_post
from database.async_db import db as db_ins

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
                        user: Annotated[User, Depends(get_current_user)],
                        db: Db = Depends(db_ins),
                        ):
    await db.add_post(autor, topic, body, user.id)
    return JSONResponse(status_code=200, content={"message": "Successful Response"})


@router.post("/dellPost/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}
             })
async def dell_post(post_id: int,
                    user: Annotated[User, Depends(get_current_user)],
                    db: Db = Depends(db_ins)):
    res = await db.dell_post(post_id, user.id)
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
                         user: Annotated[User, Depends(get_current_user)],
                         db: Db = Depends(db_ins)
                         ):
    res = await db.edit_post(post_id, autor, topic, body, user.id)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.post("/like/{post_id}",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
                 404: {"model": Message, "description": "Post not found"}}
             )
async def like_post(post_id: int, db: Db = Depends(db_ins)):
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
async def dislike_post(post_id: int, db: Db = Depends(db_ins)):
    res = await db.dislike_post(post_id)
    if res:
        return JSONResponse(status_code=200, content={"message": "Successful Response"})
    else:
        return JSONResponse(status_code=404, content={"message": "Post not found"})


@router.get("/getAllPosts",
            responses={
                200: {"model": list[Post], "description": "Successful Response"}}
            )
async def get_all_posts(db: Db = Depends(db_ins)) -> list[Post]:
    posts = await db.get_posts()
    posts = list(map(lambda x: from_db_post(x), posts))
    return posts


@router.post("/register",
             responses={
                 200: {"model": Message, "description": "Successful register"},
                 409: {"model": Message, "description": "Already exist"}}
             )
async def register_post(login: Annotated[str, Form()],
                        password: Annotated[str, Form()],
                        db: Db = Depends(db_ins)
                        ):
    u = await db.get_user(login)
    if u is None:
        await db.register_user(login, get_password_hash(password))
        return JSONResponse(status_code=200, content={"message": "Successful register"})
    else:
        return JSONResponse(status_code=409, content={"message": "Already exist"})


@router.post("/login",
             responses={
                 200: {"model": Message, "description": "Successful login"},
                 401: {"model": Message, "description": "Incorrect username or password"}}
             )
async def login_post(
        login: Annotated[str, Form()],
        password: Annotated[str, Form()],
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

    res = JSONResponse(status_code=200,
                       headers={"access_token": access_token, "token_type": "bearer"},
                       content={"message": "Successful login"})

    res.set_cookie(key="access_token", value=access_token)
    res.set_cookie(key="token_type", value="bearer")

    return res
