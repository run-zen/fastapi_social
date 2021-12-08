from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from . import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection successfully')
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print(error)
#         time.sleep(2)
#         continue


@app.get("/")
def root():
    return {"message": "Hello Ranjan from Fast API"}


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


@app.post('/posts')
def create_post(post: schemas.PostCreate, res: Response, db: Session = Depends(get_db)):
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
def delete_post(id: int, res: Response, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: schemas.PostUpdate, res: Response, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    #
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    res.status_code = status.HTTP_202_ACCEPTED
    return {"updated_post": post_query.first()}
