from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Response
from typing import List

class SocketManager:
    def __init__(self):
        self.active_connections: List[tuple[WebSocket, str]] = []

    async def connect(self, websocket: WebSocket, user: str):
        """
        Handle a new WebSocket connection.

        Parameters:
        - websocket (WebSocket): The WebSocket object representing the connection.
        - user (str): Identifier for the user associated with the connection.
        """
        await websocket.accept()
        self.active_connections.append((websocket, user))

    def disconnect(self, websocket: WebSocket, user: str):
        """
        Handle a WebSocket disconnection.

        Parameters:
        - websocket (WebSocket): The WebSocket object representing the connection.
        - user (str): Identifier for the user associated with the connection.
        """
        self.active_connections.remove((websocket, user))

    async def broadcast(self, data: dict):
        """
        Broadcast a message to all connected WebSocket clients.

        Parameters:
        - data (dict): The message to be sent as a JSON payload.
        """
        for connection in self.active_connections:
            await connection[0].send_json(data)


manager = SocketManager()

