"""
Main Application for chat app
"""
import os
script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from chat_app.api import chats, messages
from chat_app.api import users, ui, auth
from chat_app.db.base import Base, engine
import uvicorn
Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
app.include_router(ui.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(messages.router)

from chat_app.api.websocketchat import *
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)