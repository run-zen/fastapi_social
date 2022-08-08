from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import post, user, auth, vote, contact, chat, message
from app.config import settings
from twilio.rest import Client
from app import schemas

# to create tables by sqlAlchemy
# disabling it as alembic is used instead
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(contact.router)
app.include_router(chat.router)
app.include_router(message.router)


@app.get("/", )
def root():
    return {"message": "Hello from the server"}


@app.post('/send-otp')
def send_otp(data: schemas.SendMessage):
    account_sid = settings.Account_SID
    auth_token = settings.Auth_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        messaging_service_sid=settings.Messaging_Service_SID,
        body=data.message,
        to=f"+91{data.receiver}"
    )

    return {"message": 'successfully send message'}
