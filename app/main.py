from fastapi import FastAPI, Response, Request, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection successfully')
        break
    except Exception as error:
        print('Connection to database failed')
        print(error)
        time.sleep(2)
        continue

my_posts = [
    {
        "id": 1,
        "title": 'sample title',
        "content": "this is the sample content"
    }
]


def findPostById(id):
    for p in my_posts:
        if p['id'] == id:
            return p

    return None


def get_post_index(id):
    if len(my_posts) > 0:
        for i, p in enumerate(my_posts):
            if p['id'] == id:
                return i


@app.get("/")
def root():
    return {"message": "Hello Ranjan from Fast API"}


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


@app.post('/posts')
def create_post(post: Post, res: Response, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    #
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    res.status_code = status.HTTP_201_CREATED
    return {"new_post": new_post}


@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts
    # WHERE id = %s""", (str(id)))
    #
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return {"data": post}


@app.delete('/posts/{id}')
def delete_post(id: int, res: Response):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post, res: Response):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    res.status_code = status.HTTP_200_OK
    return {"updated_post": updated_post}
