import logging
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status
from ..utils import verify_password, hash_password
from .base import get_db

def handle_exception(f):
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except TypeError as e:
            return schemas.ResponseMessage(success=False, message=f"{str(e)}")
        return response
    return wrapper

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_username_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, username: str, password: str):
    hashed_password = hash_password(password)
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_friendship(db: Session, id: int):
    return db.query(models.Friend).filter(models.Friend.id == id).first()

def create_friendship(db: Session, friend_id: int, user_id: int):
    db_friend = models.Friend(friend_id=friend_id, user_id=user_id)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend

def get_friends(db: Session, user_id: int):
    return db.query(models.Friend).filter(models.Friend.user_id == user_id).all()

def get_friendship_by_users(db: Session, user_id: int, friend_id: int):
    friendship_query = db.query(models.Friend).filter((
                                                                  models.Friend.user_id == user_id and models.Friend.friend_id == friend_id) | \
                                                      (
                                                                  models.Friend.user_id == friend_id and models.Friend.friend_id == user_id))
    return friendship_query.first()

def check_is_friend(db: Session, user_id: int):
    return db.query(models.Friend).filter(models.Friend.user_id == user_id)\
            .filter(models.Friend.friend_id == user_id).first()

def get_chats_by_users(db: Session, user_id: int, friend_id: int = None):
    if friend_id is None:
        query = db.query(models.Chat)
        return query.all()
    return db.query(models.Chat).filter((models.Chat.user_id == user_id and models.Chat.friend_id == friend_id) |
                                        models.Chat.friend_id == user_id and
                                        models.Chat.user_id == friend_id).all()
def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def get_chats_all(db: Session):
    return db.query(models.Chat).all()

def create_chat(db: Session, chat: schemas.ChatCreate):
    db_chat = models.Chat(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_chat_for_users(db: Session, user_id: int, friend_id: int):
    return (
        db.query(models.Chat)
        .filter(
            ((models.Chat.friend_id == user_id) & (models.Chat.user_id == friend_id))
            | ((models.Chat.friend_id == friend_id) & (models.Chat.user_id == user_id))
        )
        .order_by(models.Chat.id)
        .all()
    )

logger = logging.getLogger(__name__)

def create_message(message: schemas.MessageCreate):
    try:
        db = next(get_db())
        db_message = models.ChatMessage(**message)
        db.add(db_message)
        db.commit()
        print("Here")
        print(db_message)
    except Exception as e:
        print(e)
    return schemas.ResponseMessage(success=True, message="Message sent successfully")

@handle_exception
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return schemas.ResponseMessage(success=True, message="Friendship deleted successfully")

@handle_exception
def delete_friendship(db: Session, friendship_id: int):
    db_friendship = db.query(models.Friend).filter(models.Friend.id == friendship_id).first()
    if not db_friendship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friendship not found")
    db.delete(db_friendship)
    db.commit()
    return schemas.ResponseMessage(success=True, message="Friendship deleted successfully")

def get_chat_messages(db: Session, chat_id: int):
    messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.chat_id == chat_id
    ).order_by(models.ChatMessage.id).all()

    return messages

def login(db, username: str, password: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return {"status" : False, "message": "User not found"}

    if not verify_password(password, db_user.hashed_password):
        return {"status": False, "message": "Incorrect Password"}

    return {"status" : True, "message": "Login successful"}