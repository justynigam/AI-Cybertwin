from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Pushes the JSON alert to all connected React clients."""
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except RuntimeError:
                pass # Client disconnected ungracefully

manager = ConnectionManager()

@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, wait for client messages if needed
            data = await websocket.receive_text() 
    except WebSocketDisconnect:
        manager.disconnect(websocket)
