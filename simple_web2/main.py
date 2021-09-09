import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root_simple_web1(id: int):
    return {"message": f"I'm simple web 2 and You are id {id}!!"}


@app.options("/")
def check():
    return {"message": "Hello checking!"}