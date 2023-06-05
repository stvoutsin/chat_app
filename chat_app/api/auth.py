from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from chat_app.db import crud
from chat_app.db import schemas
from chat_app.db.base import get_db

router = APIRouter()

@router.get("/api/current_user")
def get_user(request: Request) -> str:
    """
    Retrieve the current user from the request cookies.

    Parameters:
    - request: The incoming request object.

    Returns:
    - str: The value of the "X-Authorization" cookie.
    """
    return request.cookies.get("X-Authorization")

@router.post("/api/register")
def register_user(username: schemas.RegisterValidator,
                  response: Response) -> dict:
    """
    Register a new user.

    Parameters:
    - username: The user registration data.
    - response: The response object to set the "X-Authorization" cookie.

    Returns:
    - dict: A message indicating the successful user registration.
    """
    response.set_cookie(key="X-Authorization",
                        value=username.username, httponly=True)
    return {"message": "User registered successfully."}

@router.post("/api/login")
def login_user(user: schemas.UserLogin, response: Response,
               db: Session = Depends(get_db)) -> dict:
    """
    Login a user.

    Parameters:
    - user: The user login data.
    - response: The response object to set the "X-Authorization" cookie.
    - db: The database session dependency.

    Returns:
    - dict: A dictionary containing the authentication status and additional information.
    """
    auth = crud.login(db=db, username=user.username, password=user.password)
    if auth["status"]:
        response.set_cookie(key="X-Authorization",
                            value=user.username, httponly=True)
    return auth

@router.get("/api/logout")
def logout_user(response: Response) -> RedirectResponse:
    """
    Logout the current user.

    Parameters:
    - response: The response object to delete the "X-Authorization" cookie.

    Returns:
    - RedirectResponse: A redirect response to the home page.
    """
    response = RedirectResponse('/', status_code=302)
    response.delete_cookie(key='X-Authorization')
    return response
