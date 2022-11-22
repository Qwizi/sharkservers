from fastapi import FastAPI

from app.__version import VERSION
from app.db import database

app = FastAPI(
    version=VERSION
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def home():
    return {}
