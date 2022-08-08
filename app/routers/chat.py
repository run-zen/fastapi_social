from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy import desc, not_, text, case
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils import save_to_database
from .. import models, schemas, oauth2

router = APIRouter(
    prefix='/chats',
    tags=["Chats"]
)


@router.get('/mychats')
def get_my_chats(db: Session = Depends(get_db),
                 current_contact: schemas.ContactSchema = Depends(oauth2.get_current_contact)):
    chat = models.Chat

    query_statement = db.query(chat.participants, chat.removed_participants, chat.id, chat.last_accessed,
                               models.Contact.name.label('receiver'), models.Contact.id.label('receiver_id'),
                               models.Contact.phone_number.label('phone_number')) \
        .join(models.Contact, case(
        (models.Chat.participants[1] == current_contact.phone_number,
         models.Chat.participants[2] == models.Contact.phone_number),
        (models.Chat.participants[2] == current_contact.phone_number,
         models.Chat.participants[1] == models.Contact.phone_number),
    ), isouter=True).filter(
        not_(models.Chat.removed_participants.any(current_contact.phone_number))).filter(
        models.Chat.participants.any(current_contact.phone_number)).order_by(desc(models.Chat.last_accessed))

    return {
        "data": query_statement.all()
    }


@router.post('/', )
def create_chat(data: schemas.CreateChat, db: Session = Depends(get_db),
                current_contact: schemas.ContactSchema = Depends(oauth2.get_current_contact)):
    create_new = True
    if data.participant == current_contact.phone_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot create chat with yourself")

    receiver = db.query(models.Contact).filter(models.Contact.phone_number == data.participant).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Participant with phone number  : {data.participant} does not exists")

    participants = [data.participant, current_contact.phone_number]
    existing_chat_query = db.query(models.Chat).filter(
        models.Chat.participants.any(participants[0]) & models.Chat.participants.any(participants[1]))

    existing_chat = existing_chat_query.first()

    if existing_chat:
        if len(existing_chat.removed_participants) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Chat with the participant {data.participant} already exists")

        else:
            existing_chat_query.update({"removed_participants": [], "last_accessed": text('now()')},
                                       synchronize_session=False)
            db.commit()
            create_new = False

    new_chat = {}
    if create_new:
        chat = {"participants": participants}
        try:
            new_chat = models.Chat(**chat)
        except BaseException:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        new_chat = save_to_database(db, new_chat,
                                    unique_error_message=f"Chat with the participant {data.participant} already exists")

    else:
        new_chat = existing_chat_query.first()

    new_chat = new_chat.__dict__
    new_chat["receiver"] = receiver.name
    new_chat["receiver_id"] = receiver.phone_number

    return {
        "message": "ok from server",
        "data": new_chat,
    }


@router.post('/update_time')
def update_time(data: schemas.UpdateTime, db: Session = Depends(get_db),
                current_contact: schemas.ContactSchema = Depends(oauth2.get_current_contact)):
    update_query = db.query(models.Chat).filter(models.Chat.id == data.id)

    chat = update_query.first()

    if chat.participants.count(current_contact.phone_number) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not authorized to perform this action")

    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No chat found")

    update_query.update({"last_accessed": 'now()'}, synchronize_session=False)
    db.commit()

    return {
        "message": "ok from server",
        "data": update_query.first()
    }


@router.delete('/{chat_id}')
def delete_chat(chat_id: int, db: Session = Depends(get_db),
                current_contact: schemas.ContactSchema = Depends(oauth2.get_current_contact)):
    update_query = db.query(models.Chat).filter(models.Chat.id == chat_id)
    existing_chat: schemas.ChatSchema = update_query.first()

    if not existing_chat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Chat with the chat ID {chat_id} does not exists")

    if existing_chat.removed_participants.count(current_contact.phone_number) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Chat already deleted")

    if existing_chat.participants.count(current_contact.phone_number) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"You are not authorized to delete this chat")

    updated_chat = {
        "removed_participants": existing_chat.removed_participants,
    }
    updated_chat["removed_participants"].append(current_contact.phone_number)

    update_query.update(updated_chat, synchronize_session=False)
    db.commit()

    return {
        "updated_chat": update_query.first()
    }
