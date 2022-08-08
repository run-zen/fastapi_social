from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from .. import utils, oauth2, responseSchemas, schemas

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=responseSchemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    if not utils.verify_password(plain_password=user_credentials.password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    # create token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {'access_token': access_token, "token_type": 'bearer'}


@router.post('/contacts/login', response_model=responseSchemas.ContactLogin)
def contact_login(user_credentials: schemas.ContactLogin, res: Response, db: Session = Depends(get_db)):
    print(user_credentials)
    contact = db.query(models.Contact).filter(models.Contact.phone_number == user_credentials.phone_number).first()

    if not contact:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    if not utils.verify_password(plain_password=user_credentials.password, hashed_password=contact.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    # create token
    # return token

    access_token = oauth2.create_access_token(data={"phone_number": contact.phone_number})
    res.set_cookie(key='jwt',value=access_token)

    return {'access_token': access_token, "token_type": 'bearer', "user": contact}
