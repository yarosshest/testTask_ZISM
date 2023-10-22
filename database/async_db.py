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

from database.Db_objects import Post, Base, User

meta = MetaData()

p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')

config = configparser.ConfigParser()
config.read(p)

BDCONNECTION = config['DEFAULT']["BDCONNECTION"]


async def session_gen(session_maker: async_sessionmaker):
    while True:
        async with session_maker() as async_session:
            await async_session.begin()
            try:
                yield async_session
            finally:
                async_session.close()


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

    async_sessionmaker = async_sessionmaker(engine, expire_on_commit=True)

    async def get_session(self) -> AsyncSession:
        async with self.async_sessionmaker() as async_session:
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

    async def dell_post(self, post_id: int, user_id: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Post).where(Post.id == post_id, Post.user_id == user_id)
            result = await session.execute(q)
            post = result.scalars().unique().first()
            if post is None:
                return False
            else:
                await session.delete(post)
                return True
        finally:
            await session.commit()
            await session.close()

    async def add_post(self, autor: str, topic: str, body: str, user_id: int) -> None:
        session = await self.get_session()
        try:
            post = Post(autor, topic, body, user_id)
            session.add(post)
            await session.flush()
            await session.commit()
        finally:
            await session.close()

    async def edit_post(self, post_id: int, autor: str, topic: str, body: str, user_id: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Post).where(Post.id == post_id, Post.user_id == user_id)
            result = await session.execute(q)
            post = result.scalars().unique().first()
            if post is None:
                return False
            else:
                post.autor = autor
                post.topic = topic
                post.body = body
                await session.commit()
                return True
        finally:
            await session.close()

    async def get_user_posts(self, user_id: int) -> List[Post]:
        session = await self.get_session()
        try:
            q = select(Post).where(Post.user_id == user_id)
            posts = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in posts:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def get_posts(self) -> List[Post]:
        session = await self.get_session()
        try:
            q = select(Post)
            posts = (await session.execute(q)).scalars().unique().fetchall()
            res = []
            for i in posts:
                session.expunge(i)
                res.append(i)
            return res
        finally:
            await session.close()

    async def get_post(self, post_id: int) -> Post | None:
        session = await self.get_session()
        try:
            q = select(Post).where(Post.id == post_id)
            post = (await session.execute(q)).scalars().unique().first()
            if post is None:
                return None
            else:
                session.expunge(post)
                return post
        finally:
            await session.close()

    async def like_post(self, post_id: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Post).where(Post.id == post_id)
            result = await session.execute(q)
            post = result.scalars().unique().first()
            if post is None:
                return False
            else:
                post.likes += 1
                await session.commit()
                return True
        finally:
            await session.close()

    async def dislike_post(self, post_id: int) -> bool:
        session = await self.get_session()
        try:
            q = select(Post).where(Post.id == post_id)
            result = await session.execute(q)
            post = result.scalars().unique().first()

            if post is None:
                return False
            else:
                post.likes -= 1
                await session.commit()
                return True
        finally:
            await session.close()

    async def get_user(self, username: str) -> User | None:
        session = await self.get_session()
        try:
            q = select(User).where(User.username == username)
            result = await session.execute(q)
            u = result.scalars().unique().first()
            session.expunge_all()

            if u is None:
                return None
            else:
                return u
        finally:
            await session.close()

    async def register_user(self, username: str, h_password: str):
        session = await self.get_session()
        try:
            u = User(username=username, hashed_password=h_password)
            session.add(u)
            await session.commit()
        finally:
            await session.close()


db = DataBase()

if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(DataBase.init_db())
