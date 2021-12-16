from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import responseSchemas, models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@router.get('/', response_model=responseSchemas.MultiplePost, )
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@router.post('/', response_model=responseSchemas.SinglePost)
def create_post(post: schemas.PostCreate, res: Response, db: Session = Depends(get_db),
                current_user: object = Depends(oauth2.get_current_user)):
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
    return {"data": new_post, "message": 'Post successfully created'}


@router.get("/{id}", response_model=responseSchemas.SinglePost)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts
    # WHERE id = %s""", (str(id)))
    #
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return {"data": post}


@router.delete('/{id}')
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


@router.put('/{id}', response_model=responseSchemas.SinglePost)
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
    return {
        "data": post_query.first(),
        "message": 'Post updated successfully'
    }
