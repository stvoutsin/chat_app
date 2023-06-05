from __future__ import annotations
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chat_app.db import crud
from chat_app.db import schemas
from chat_app.db.base import SessionLocal

router = APIRouter()


# Dependency: get database session
def get_db() -> Session:
    """
    Get a database session dependency.

    Returns:
    - Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/api/chats/", response_model=schemas.Chat)
def create_chat(chat: schemas.ChatCreate, db: Session = Depends(get_db)) -> schemas.Chat:
    """
    Create a new chat.

    Parameters:
    - chat: The chat data to be created.
    - db: The database session dependency.

    Returns:
    - schemas.Chat: The created chat data.
    """
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

    existing_chat = crud.get_chat_for_users(db, user_id=chat.user_id, friend_id=chat.friend_id)
    if existing_chat is not None:
        raise HTTPException(status_code=404, detail="Chat already exists")

    # Create new chat
    return crud.create_chat(db=db, chat=chat)


@router.get("/api/chats/{chat_id}", response_model=schemas.Chat)
def read_chat(chat_id: int, db: Session = Depends(get_db)) -> schemas.Chat:
    """
    Read a chat by its ID.

    Parameters:
    - chat_id: The ID of the chat.
    - db: The database session dependency.

    Returns:
    - schemas.Chat: The chat data.
    """
    chat = crud.get_chat(db, chat_id=chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.get("/api/chats/", response_model=List[schemas.Chat])
def read_chats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[schemas.Chat]:
    """
    Read all chats.

    Parameters:
    - skip: Number of chats to skip (for pagination).
    - limit: Maximum number of chats to retrieve (for pagination).
    - db: The database session dependency.

    Returns:
    - List[schemas.Chat]: A list of chat data.
    """
    chats = crud.get_chats_all(db)
    return chats


@router.get("/api/chats/user/{user_id}", response_model=List[schemas.Chat])
def get_chats_by_user(user_id: int, db: Session = Depends(get_db)) -> List[schemas.Chat]:
    """
    Get all chats for a user.

    Parameters:
    - user_id: The ID of the user.
    - db: The database session dependency.

    Returns:
    - List[schemas.Chat]: A list of chat data.
    """
    # Check if the friendship exists
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Friendship not found")
    # Retrieve all chats between the two users
    return crud.get_chats_by_users(db, user_id=user_id)


@router.get("/api/chats/user/{user_id}/friend/{friend_id}", response_model=List[schemas.Chat])
def read_chat_history(user_id: int, friend_id: int, db: Session = Depends(get_db)) -> List[schemas.Chat]:
    """
    Read the chat history between two users.

    Parameters:
    - user_id: The ID of the user.
    - friend_id: The ID of the friend.
    - db: The database session dependency.

    Returns:
    - List[schemas.Chat]: A list of chat data.
    """
    # Check if the friendship exists
    friendship = crud.get_friendship_by_users(db, user_id=user_id, friend_id=friend_id)
    if friendship is None:
        raise HTTPException(status_code=404, detail="Friendship not found")
    # Retrieve all chats between the two users
    return crud.get_chats_by_users(db, user_id=user_id, friend_id=friend_id)
