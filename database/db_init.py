import configparser
import pathlib
from asyncio import get_event_loop

from database.async_db import DataBase as Db


async def db_init():
    db = Db()
    await db.init_db()

    p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
    config = configparser.ConfigParser()
    config.read(p)

    full = config['DEFAULT']['INITFULL'] == 'False'

    if full:
        await db.add_post("test1", "test1", "test1")
        await db.add_post("test2", "test2", "test2")
        await db.add_post("test3", "test3", "test3")

        config['DEFAULT']['INITFULL'] = 'True'
        with open('config.ini', 'w') as configfile:  # save
            config.write(configfile)

if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(db_init())
