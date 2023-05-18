import websockets
import asyncio
import json
import secrets


class WebSocketServer:
    def __init__(self, port, host) -> None:
        self.events = {}
        self.port = port
        self.host = host

    async def send_message_to_subscribers(self, message, key):
        # Enviar mensaje a cada cliente suscrito
        try:
            subscriptions = self.events[key]
            for subscriber in subscriptions:
                await subscriber.send(message)
        except KeyError:
            pass
        except websockets.exceptions.ConnectionClosedOK:
            pass

    async def join_sub(self, key, websocket):
        sub = self.events[key]
        sub.append(websocket)

    def new_sub(self):
        key = secrets.token_urlsafe(16)
        self.events[key] = []
        return key

    def delete_sub(self, key):
        del self.events[key]

    # Función para manejar las conexiones WebSocket
    async def handle_connection(self, websocket):
        # Loop principal de manejo de conexiones
        try:
            async for message in websocket:
                # Parsear el mensaje recibido desde el cliente
                data = json.loads(message)
                match data["type"]:
                    case "join":
                        key = data["key"]
                        await self.join_sub(key, websocket)
        except websockets.exceptions.ConnectionClosedOK:
            pass

    async def main(self):
        # Iniciar el servidor WebSocket
        async with websockets.serve(self.handle_connection, self.host, self.port):
            print("algo")
            await asyncio.Future()  # Correr el servidor para siempre


server = WebSocketServer(8765, "localhost:")
