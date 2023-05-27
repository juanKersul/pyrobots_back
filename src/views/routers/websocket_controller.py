from fastapi import WebSocket
from fastapi import APIRouter
from fastapi import WebSocketDisconnect
from fastapi import Depends
from controllers.security.tokens import authorize_token
from controllers.websockets2.websocket_services import server
import json

websocket_endpoints = APIRouter()


@websocket_endpoints.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            match data["type"]:
                case "watch":
                    await server.join_sub(data["key"], websocket)
                case _:
                    await websocket.send_json({"error": "No existe el tipo de evento"})
        except WebSocketDisconnect:
            pass
        except json.decoder.JSONDecodeError:
            await websocket.send_json({"error": "No es un json valido"})
