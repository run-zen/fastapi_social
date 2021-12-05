from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello Ranjan from Fast API"}


@app.get('/posts')
def get_posts():
    return {"data": []}


@app.post('/posts')
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"Title {payload['title']} Content: {payload['content']}"}
