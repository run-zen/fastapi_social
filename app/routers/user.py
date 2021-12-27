from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DBAPIError
from .. import responseSchemas, models, schemas
from app.utils import hash_password
from app.database import get_db

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=responseSchemas.SingleUser)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except DBAPIError as err:
        print(str(err.args))
        if "psycopg2.errors.UniqueViolation" in str(err.args):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists")
    except BaseException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong")

    return {
        "data": new_user,
        "message": "User Created Successfully"
    }


@router.get('/{id}', response_model=responseSchemas.SingleUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} does not exists")

    return {
        "data": user,
        "message": "OK from server"
    }
