from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .. import database, oauth2, models, schemas

router = APIRouter(
    prefix='/vote',
    tags=["Vote"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(user_vote: schemas.Vote, res: Response, db: Session = Depends(database.get_db),
         current_user: schemas.UserSchema = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == user_vote.post_id)
    found_post = post_query.first()

    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {user_vote.post_id} does not exists")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == user_vote.post_id,
                                              models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if user_vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {user_vote.post_id}")

        new_vote = models.Vote(post_id=user_vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exists")

        vote_query.delete(synchronize_session=False)
        db.commit()
        res.status_code = status.HTTP_204_NO_CONTENT
        return {"message": 'Successfully deleted vote'}
