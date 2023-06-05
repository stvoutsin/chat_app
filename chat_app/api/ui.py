import sys
sys.path.append("../..") # Adds higher directory to python modules path.
from fastapi import APIRouter
router = APIRouter()
from fastapi import Depends, HTTPException, Request, FastAPI
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from chat_app.db import crud
from chat_app.db.base import get_db
from datetime import datetime
import os
script_dir = os.path.dirname(__file__)
templates_abs_file_path = os.path.join(script_dir, "../templates/")


templates = Jinja2Templates(directory=templates_abs_file_path)

app = FastAPI()

@router.get("/")
def get_home(request: Request, db: Session = Depends(get_db)) -> templates.TemplateResponse:
    """
    Get the home page.

    Parameters:
    - request: The incoming request object.
    - db: The database session dependency.

    Returns:
    - templates.TemplateResponse: The rendered template response for the home page.
    """
    current_user = request.cookies.get("X-Authorization")
    chats = []
    users = []
    if current_user:
        db_user = crud.get_user_by_username(db, username=current_user)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        chats = crud.get_chats_by_users(db, user_id=db_user.id)
        users = {}
        for chat in chats:
            users[chat.user_id] = crud.get_username_by_id(db, chat.user_id)
            users[chat.friend_id] = crud.get_username_by_id(db, chat.friend_id)
    return templates.TemplateResponse("home.html", {"current_user" : current_user, "request": request, "chats": chats,
                                                    "users": users})


@router.get("/{chat_id}")
def get_chat_page(chat_id: int, request: Request,
                  db: Session = Depends(get_db)) -> templates.TemplateResponse:
    """
    Get the chat page for a specific chat ID.

    Parameters:
    - chat_id: The ID of the chat.
    - request: The incoming request object.
    - db: The database session dependency.

    Returns:
    - templates.TemplateResponse: The rendered template response for the chat page.
    """
    db_chat = crud.get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat page not found")
    db_user = crud.get_user(db, user_id=db_chat.user_id)
    db_friend = crud.get_user(db, user_id=db_chat.friend_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User #1 not found")
    if not db_friend:
        raise HTTPException(status_code=404, detail="User #2 not found")

    current_user = request.cookies.get("X-Authorization")
    if current_user != db_user.username and current_user != db_friend.username:
        raise HTTPException(status_code=401, detail="Not authorized to view this chat")

    friend_id = db_friend.id if current_user != db_friend.username else db_user.id
    user_id = db_friend.id if current_user == db_friend.username else db_user.id
    users = {db_user.id : db_user, db_friend.id: db_friend}
    db_chat_messages = crud.get_chat_messages(db, chat_id)
    return templates.TemplateResponse("chat.html", {"datetime": datetime, "chat": db_chat,
                                                    "messages": db_chat_messages,
                                                    "users" : users, "request" : request,
                                                    "user_id" : user_id,
                                                    "current_user": current_user,
                                                    "friend_id": friend_id})

