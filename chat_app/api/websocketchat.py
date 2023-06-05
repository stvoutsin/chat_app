from chat_app.db.base import Base, engine
from chat_app.ws import manager
from sqlalchemy.orm import Session
from chat_app.db import crud
from chat_app.db.base import get_db
import datetime
Base.metadata.create_all(bind=engine)
from chat_app.main import app
from chat_app.tasks import send_message
from fastapi import WebSocket, WebSocketDisconnect, Depends
from chat_app.utils import ai_rewrite_message
from chat_app.config import tone

@app.websocket("/ws/chat")
async def chat(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for handling chat communication.

    Parameters:
    - websocket: The WebSocket connection object.
    - db: The database session dependency.
    """

    sender = websocket.cookies.get("X-Authorization")
    if sender:
        await manager.connect(websocket, sender)
        response = {
            "sender": sender,
            "message": "got connected",
            "created_at": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }
        await manager.broadcast(response)
        try:
            while True:
                data = await websocket.receive_json()
                if all(key in data for key in ('chat_id', 'sender_id',"message")):
                    creation_timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    rewritten_message =  ai_rewrite_message(data['message'], tone)
                    message = {'sender_id': data['sender_id'],
                               'message': rewritten_message,
                               'chat_id': data['chat_id'],
                               'created_at': creation_timestamp}

                    send_message.delay(message=message)
                    data = {
                        'sender': crud.get_username_by_id(db=db, user_id=data['sender_id']).username,
                        "message": rewritten_message,
                        "created_at": creation_timestamp,
                        "db_status" : {"status": True, "message": "Message sent successfully"}
                    }
                await manager.broadcast(data)
        except WebSocketDisconnect:
            manager.disconnect(websocket, sender)
            response['message'] = "left"
            await manager.broadcast(response)
