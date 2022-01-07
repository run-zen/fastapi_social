from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from .. import responseSchemas, models, schemas, oauth2
from app.database import get_db
from typing import Optional

from ..controllers.post_controller import get_all_posts, get_generic_post_query

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@router.get('/', response_model=responseSchemas.MultiplePost, )
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, sortBy: str = 'date', user_id: int = None,
              search: Optional[str] = None):
    return get_all_posts(db, limit, skip, sortBy, user_id, search)


@router.get("/{id}", response_model=responseSchemas.SinglePost)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = get_generic_post_query(db).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return {"data": post}


# PROTECTED ROUTES BELOW

@router.post('/', response_model=responseSchemas.SinglePost)
def create_post(post: schemas.PostCreate, res: Response, db: Session = Depends(get_db),
                current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    post_data: dict = post.dict()
    post_data['user_id'] = current_user.id
    new_post = models.Post(**post_data)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    res.status_code = status.HTTP_201_CREATED
    return {"data": new_post, "message": 'Post successfully created'}


@router.delete('/{id}')
def delete_post(id: int, res: Response, db: Session = Depends(get_db),
                current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=responseSchemas.SinglePost)
def update_post(id: int, post: schemas.PostUpdate, res: Response, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    res.status_code = status.HTTP_202_ACCEPTED
    return {
        "data": post_query.first(),
        "message": 'Post updated successfully'
    }
