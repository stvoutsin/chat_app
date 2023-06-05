from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chat_app.db import crud
from chat_app.db import schemas
from chat_app.db.base import get_db
router = APIRouter()


@router.get("/api/chats/{chat_id}/messages", response_model=List[schemas.ChatMessage])
def read_chat(chat_id: int, db: Session = Depends(get_db)) -> List[schemas.ChatMessage]:
    """
    Read all messages for a chat.

    Parameters:
    - chat_id: The ID of the chat.
    - db: The database session dependency.

    Returns:
    - List[schemas.ChatMessage]: A list of chat message data.
    """
    chat_messages = crud.get_chat_messages(db, chat_id=chat_id)
    if chat_messages is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat_messages


@router.post("/api/chats/{chat_id}/messages", response_model=schemas.ResponseMessage)
def create_message(chat_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)) -> schemas.ResponseMessage:
    """
    Create a message for a chat.

    Parameters:
    - chat_id: The ID of the chat.
    - message: The message data to be created.
    - db: The database session dependency.

    Returns:
    - schemas.ResponseMessage: The response message.
    """
    try:
        # Check if the chat exists
        chat = crud.get_chat(db, chat_id)
        if chat is None:
            raise HTTPException(status_code=404, detail="Chat does not exist")

        # Check if the friendship exists
        friendship = crud.get_friendship_by_users(db, user_id=chat.user_id, friend_id=chat.friend_id)
        if friendship is None:
            raise HTTPException(status_code=404, detail="Friendship not found")

        db_user = crud.get_user(db, user_id=chat.user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        db_friend = crud.get_user(db, user_id=chat.friend_id)
        if db_friend is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Create new message
        return crud.create_message(db=db, message=message, chat_id=chat_id)
    except Exception as e:
        print(str(e))

    return None
