import os

import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from database.db_init import db_init
from fastapi.security import OAuth2PasswordBearer
from app.routers import web, api

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

app.include_router(web.router)
app.include_router(api.router)

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")

app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")


def app_main():
    db_init()
    uvicorn.run(app, host="0.0.0.0", port=8031)
    # uvicorn.run('app.app.main:app', host="0.0.0.0", port=8031, workers=4)


if __name__ == "__main__":
    app_main()
