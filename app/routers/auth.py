from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.schemas import UserLogin
from .. import utils

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    if not utils.verify_password(plain_password=user_credentials.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')

    # create token
    # return token

    return {'token': 'example token'}
