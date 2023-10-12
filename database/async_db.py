from __future__ import annotations
import tracemalloc
import asyncio
from typing import List, Sequence

from sqlalchemy import NullPool, delete, MetaData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager

from random import choice

from database.Db_objects import Post, Base

import configparser
import pathlib

meta = MetaData()

p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')

config = configparser.ConfigParser()
config.read(p)

BDCONNECTION = config['DEFAULT']["BDCONNECTION"]


def async_to_tread(fun):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(fun(*args, **kwargs))
        loop.close()

    return wrapper


async def get_session():
    engine = create_async_engine(
        BDCONNECTION,
        echo=False,
        poolclass=NullPool,
    )
    async with async_sessionmaker(engine, expire_on_commit=True)() as async_session:
        await async_session.begin()
        yield async_session


class AsyncHandler:
    @staticmethod
    async def init_db() -> None:
        engine = create_async_engine(
            BDCONNECTION,
            echo=False,
            poolclass=NullPool,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await engine.dispose()

    @staticmethod
    async def dell_post(session: AsyncSession, post_id: int) -> bool:
        q = select(Post).where(Post.id == post_id)
        result = await session.execute(q)
        post = result.scalars().unique().first()
        if post is None:
            await session.commit()
            return False
        else:
            await session.delete(post)
            await session.commit()
            return True

    @staticmethod
    async def add_post(session: AsyncSession, autor, topic, body: str) -> None:
        post = Post(autor, topic, body)
        session.add(post)
        await session.flush()
        await session.commit()

    @staticmethod
    async def edit_post(session: AsyncSession, post_id: int, autor, topic, body: str) -> bool:
        q = select(Post).where(Post.id == post_id)
        result = await session.execute(q)
        post = result.scalars().unique().first()
        if post is None:
            await session.commit()
            return False
        else:
            post.autor = autor
            post.topic = topic
            post.body = body
            await session.commit()
            return True

    @staticmethod
    async def get_posts(session: AsyncSession) -> List[Post]:
        q = select(Post)
        posts = (await session.execute(q)).scalars().unique().fetchall()
        res = []
        for i in posts:
            session.expunge(i)
            res.append(i)
        await session.commit()
        return res

    @staticmethod
    async def get_post(session: AsyncSession, post_id: int) -> Post | None:
        q = select(Post).where(Post.id == post_id)
        post = (await session.execute(q)).scalars().unique().first()
        if post is None:
            await session.commit()
            return None
        else:
            session.expunge(post)
            await session.commit()
            return post


    @staticmethod
    async def like_post(session: AsyncSession, post_id: int) -> bool:
        q = select(Post).where(Post.id == post_id)
        result = await session.execute(q)
        post = result.scalars().unique().first()
        if post is None:
            await session.commit()
            return False
        else:
            post.likes += 1
            await session.commit()
            return True

    @staticmethod
    async def dislike_post(session: AsyncSession, post_id: int) -> bool:
        q = select(Post).where(Post.id == post_id)
        result = await session.execute(q)
        post = result.scalars().unique().first()

        if post is None:
            await session.commit()
            return False
        else:
            post.likes -= 1
            await session.commit()
            return True


if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(AsyncHandler.init_db())
    # asyncio.run(AsyncHandler.add_post("test1", "test1", "test1"))
    # asyncio.run(AsyncHandler.add_post("test2", "test2", "test2"))
    # asyncio.run(AsyncHandler.add_post("test3", "test3", "test3"))
