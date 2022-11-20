from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {}


@app.get("/dupa")
def dupa():
    return {"msg": "dupa"}
