from fastapi import WebSocket, WebSocketDisconnect
import secrets


class SubscriptionServer:
    def __init__(self) -> None:
        self.events = {}

    async def send_message_to_subscribers(self, message, key):
        # Enviar mensaje a cada cliente suscrito
        try:
            print(self.events[key])
            for subscriber in self.events[key]:
                await subscriber.send_json(message)
        except KeyError:
            pass
        except WebSocketDisconnect:
            pass

    async def join_sub(self, key, websocket: WebSocket):
        try:
            sub = self.events[key]
            sub.append(websocket)
        except KeyError:
            await websocket.send_json({"error": "No existe el evento"})
        except WebSocketDisconnect:
            pass

    def new_sub(self):
        key = secrets.token_urlsafe(16)
        self.events[key] = []
        return key

    def delete_sub(self, key):
        del self.events[key]


server = SubscriptionServer()
