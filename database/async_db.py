from __future__ import annotations

import asyncio
import configparser
import pathlib
import tracemalloc
from typing import List

from sqlalchemy import NullPool, MetaData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from database.Db_objects import Post, Base

meta = MetaData()

p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')

config = configparser.ConfigParser()
config.read(p)

BDCONNECTION = config['DEFAULT']["BDCONNECTION"]


class DataBase:
    def __init__(self):
        print("db class inited")

    def __call__(self):
        return self

    engine = create_async_engine(
        BDCONNECTION,
        echo=False,
        poolclass=NullPool,
    )

    async def get_session(self) -> AsyncSession:
        async with async_sessionmaker(self.engine, expire_on_commit=True)() as async_session:
            await async_session.begin()
            return async_session

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

    async def dell_post(self, post_id: int) -> bool:
        session = await self.get_session()
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

    async def add_post(self, autor, topic, body: str) -> None:
        session = await self.get_session()
        post = Post(autor, topic, body)
        session.add(post)
        await session.flush()
        await session.commit()

    async def edit_post(self, post_id: int, autor, topic, body: str) -> bool:
        session = await self.get_session()
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

    async def get_posts(self) -> List[Post]:
        session = await self.get_session()
        q = select(Post)
        posts = (await session.execute(q)).scalars().unique().fetchall()
        res = []
        for i in posts:
            session.expunge(i)
            res.append(i)
        await session.commit()
        return res

    async def get_post(self, post_id: int) -> Post | None:
        session = await self.get_session()
        q = select(Post).where(Post.id == post_id)
        post = (await session.execute(q)).scalars().unique().first()
        if post is None:
            await session.commit()
            return None
        else:
            session.expunge(post)
            await session.commit()
            return post

    async def like_post(self, post_id: int) -> bool:
        session = await self.get_session()
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

    async def dislike_post(self, post_id: int) -> bool:
        session = await self.get_session()
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


db = DataBase()

if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(DataBase.init_db())
