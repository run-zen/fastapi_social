from passlib.context import CryptContext
from sqlalchemy.exc import DBAPIError
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def save_to_database(db, data, unique_error_message="Unique constraint error"):
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except DBAPIError as err:
        if "psycopg2.errors.UniqueViolation" in str(err.args):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unique_error_message)
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong")

    except BaseException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong")
