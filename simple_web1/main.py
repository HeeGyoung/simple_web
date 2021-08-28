from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root_simple_web1():
    return {"message": "I'm simple web 1 !!"}


@app.options("/")
def check():
    return {"message": "Hello checking!"}