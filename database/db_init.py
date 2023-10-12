import asyncio
import configparser
import pathlib

from database.async_db import AsyncHandler as db
from database.async_db import get_session
from asyncio import get_event_loop


async def db_init():
    await db.init_db()

    p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
    config = configparser.ConfigParser()
    config.read(p)

    full = config['DEFAULT']['INITFULL'] == 'False'

    if full:
        gen = get_session()
        s = anext(gen)
        await db.add_post(await s, "test1", "test1", "test1")
        gen = get_session()
        s = anext(gen)
        await db.add_post(await s, "test2", "test2", "test2")
        gen = get_session()
        s = anext(gen)
        await db.add_post(await s, "test3", "test3", "test3")

        config['DEFAULT']['INITFULL'] = 'True'
        with open('config.ini', 'w') as configfile:  # save
            config.write(configfile)

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(db_init())
