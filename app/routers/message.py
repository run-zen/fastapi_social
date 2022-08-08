from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, desc
from app.database import get_db
from app.utils import save_to_database
from .. import models, schemas, oauth2

router = APIRouter(
    prefix='/message',
    tags=['Message']
)


@router.post('/by_chat_id')
def get_messages(data: schemas.GetMessage, db: Session = Depends(get_db),
                 current_contact: schemas.ContactSchema = Depends(oauth2.get_current_contact)):
    chats = db.query(models.Message).filter(models.Message.chat_id == data.chat_id).order_by(
        models.Message.created_at).all()
    return {
        "message": 'ok from server',
        "data": chats
    }


@router.post('/create_message')
def create_message(data: schemas.CreateMessage, db: Session = Depends(get_db),
                   current_contact: schemas.ContactSchema = Depends(oauth2.get_current_contact)):
    new_message = models.Message(**data.dict())

    update_query = db.query(models.Chat).filter(models.Chat.id == data.chat_id)

    chat = update_query.first()

    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chat found")

    update_query.update({"last_accessed": 'now()'}, synchronize_session=False)
    db.commit()
    new_message = save_to_database(db, new_message, unique_error_message='')

    return {
        "message": 'ok from server',
        "data": new_message
    }


@router.post('/by_id')
def get_message_by_id(data: schemas.GetMessageByID, db: Session = Depends(get_db),
                      current_contact: schemas.ContactSchema = Depends(oauth2.get_current_contact)):
    message = db.query(models.Message).filter(models.Message.id == data.id).first()

    if not message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid message id")

    if not (message.sender_id == current_contact.id or message.receiver_id == current_contact.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized to view message")

    return {
        "message": 'ok from server',
        "data": message
    }
