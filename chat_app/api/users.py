import sys
sys.path.append("../..") # Adds higher directory to python modules path.
from fastapi import APIRouter
from typing import List

router = APIRouter()
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from chat_app.db import crud, models
from chat_app.db import schemas
from chat_app.db.base import get_db
from chat_app.utils import hash_password

router = APIRouter()


@router.post("/api/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    """
    Create a new user.

    Parameters:
    - user: The user data to be created.
    - db: The database session dependency.

    Returns:
    - schemas.User: The created user data.
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = crud.create_user(db=db, username=user.username, password=user.password)
    return db_user


@router.get("/api/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    """
    Read a user by ID.

    Parameters:
    - user_id: The ID of the user.
    - db: The database session dependency.

    Returns:
    - schemas.User: The user data.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/api/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[schemas.User]:
    """
    Read all users.

    Parameters:
    - skip: The number of users to skip.
    - limit: The maximum number of users to retrieve.
    - db: The database session dependency.

    Returns:
    - List[schemas.User]: A list of user data.
    """
    users = crud.get_users(db)
    return users


@router.put("/api/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate,
                current_user: models.User = Depends(hash_password),
                db: Session = Depends(get_db)) -> schemas.User:
    """
    Update a user by ID.

    Parameters:
    - user_id: The ID of the user.
    - user: The updated user data.
    - current_user: The current user data.
    - db: The database session dependency.

    Returns:
    - schemas.User: The updated user data.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="Not authorized to update this user")
    if user.password:
        hashed_password = hash_password(user.password)
        user.password = hashed_password
    return crud.update_user(db=db, db_user=db_user, user=user)


@router.post("/api/users/{user_id}/friends", response_model=schemas.Friend)
async def create_friend(user_id: int, user: schemas.UserID, db: Session = Depends(get_db)) -> schemas.Friend:
    """
    Create a friendship between two users.

    Parameters:
    - user_id: The ID of the user.
    - user: The friend data.
    - db: The database session dependency.

    Returns:
    - schemas.Friend: The created friendship data.
    """
    friend_id = user.id
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_friend = crud.get_user(db, user_id=friend_id)
    if db_friend is None:
        raise HTTPException(status_code=404, detail="Friend not found")

    db_friendship = crud.get_friendship_by_users(db=db, user_id=user_id, friend_id=friend_id)
    if db_friendship is not None:
        raise HTTPException(status_code=404, detail="Users are already friends")

    return crud.create_friendship(db=db, user_id=user_id, friend_id=friend_id)


@router.get("/api/users/{user_id}/friends", response_model=List[schemas.Friend])
def read_friends_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[schemas.Friend]:
    """
    Read all friends for a user.

    Parameters:
    - user_id: The ID of the user.
    - skip: The number of friends to skip.
    - limit: The maximum number of friends to retrieve.
    - db: The database session dependency.

    Returns:
    - List[schemas.Friend]: A list of friend data.
    """
def read_friends_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    friends = crud.get_friends(db, user_id=user_id)
    return friends


@router.delete("/api/users/{user_id}/friends/{friend_id}", response_model=schemas.ResponseMessage)
def delete_friend(user_id: int, friend_id: int, db: Session = Depends(get_db)) -> schemas.ResponseMessage:
    """
    Delete a friendship between two users.

    Parameters:
    - user_id: The ID of the user.
    - friend_id: The ID of the friend.
    - db: The database session dependency.

    Returns:
    - schemas.ResponseMessage: The response message.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_friend = crud.get_user(db, user_id=friend_id)
    if db_friend is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_friendship = crud.get_friendship_by_user_ids(db, user_id=user_id, friend_id=friend_id)
    if db_friendship is None:
        raise HTTPException(status_code=404, detail="Users are not friends")
    return crud.delete_friendship(db=db, friendship_id=db_friendship.id)


@router.delete("/api/users/{user_id}", response_model=schemas.ResponseMessage)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> schemas.ResponseMessage:
    """
    Delete a user by ID.

    Parameters:
    - user_id: The ID of the user.
    - db: The database session dependency.

    Returns:
    - schemas.ResponseMessage: The response message.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_is_friend = crud.check_is_friend(db, user_id=user_id)
    if db_is_friend is not None:
        raise HTTPException(status_code=404, detail="User is a friend, can not be deleted")
    return crud.delete_user(db=db, db_user=db_user)
