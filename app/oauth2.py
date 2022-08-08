from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_DAYS = settings.access_token_expire_days


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={'WWW-Authenticate': "Bearer"})

    token_data = verify_access_token(token=token, credentials_exception=credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User does not exists")

    return user


def verify_contact_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_number: str = payload.get('phone_number')

        if phone_number is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=phone_number)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_contact(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={'WWW-Authenticate': "Bearer"})

    token_data = verify_contact_token(token=token, credentials_exception=credentials_exception)

    contact = db.query(models.Contact).filter(models.Contact.phone_number == token_data.id).first()

    if not contact:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User does not exists")

    return contact
