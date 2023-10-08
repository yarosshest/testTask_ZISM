from database.async_db import AsyncHandler as db
from asyncio import get_event_loop


def db_init():
    loop = get_event_loop()
    loop.run_until_complete(db.init_db())


if __name__ == '__main__':
    db_init()
