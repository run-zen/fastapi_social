from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from .. import responseSchemas, models, schemas, oauth2
from app.utils import hash_password, save_to_database
from app.database import get_db

router = APIRouter(
    prefix='/contacts',
    tags=["Contacts"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=responseSchemas.SingleContact)
def create_contact(contact: schemas.ContactCreate, res: Response, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = hash_password(contact.password)
    contact.password = hashed_password
    contact.name = contact.phone_number
    new_contact = models.Contact(**contact.dict())
    new_contact = save_to_database(db, new_contact, unique_error_message="Contact already exists")
    access_token = oauth2.create_access_token(data={"phone_number": contact.phone_number})
    res.set_cookie(key='jwt', value=access_token)

    return {
        "data": new_contact,
        "access_token": access_token,
        "token_type": 'bearer',
        "message": "Contact Created Successfully"
    }


@router.get('/me', response_model=responseSchemas.SingleContact)
def get_me(current_contact: schemas.ContactSchema = Depends(oauth2.get_current_contact)):
    return {
        "data": current_contact,
        "message": "OK from server"
    }


@router.get('/{phone_number}', response_model=responseSchemas.SingleContact)
def get_contact(phone_number: str, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.phone_number == phone_number).first()

    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Contact with phone number : {phone_number} does not exists")

    return {
        "data": contact,
        "message": "OK from server"
    }
