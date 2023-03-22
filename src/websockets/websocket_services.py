from typing import Dict
from fastapi import WebSocket
from crud.match_service import add_player, remove_player
from starlette.websockets import WebSocketState


class ConnectionManager:
    """
    Handler of socket connections
    """

    def __init__(self):
        self.active_connections: Dict[int, Dict[str, WebSocket]] = {}
        self.in_match: Dict[int, Dict[str, str]] = {}

    async def connect(self, websocket: WebSocket, id_game: int, tkn: str, id_robot:int):
        msg = add_player(id_game, tkn, id_robot)
        user_name = msg.split(":")[0]
        try:
            await websocket.accept()
            if ":" not in msg:
                raise (msg)
            if id_game in self.active_connections:  # Exist game in active_connections
                self.active_connections[id_game].update({user_name: websocket})
                self.in_match[id_game].update({user_name: msg})
            else:
                self.active_connections[id_game] = {user_name: websocket}
                self.in_match[id_game] = {user_name: msg}
            broadcast_msg = ""
            it = 0
            for user in list(self.in_match[id_game].keys()):
                if (it > 0):
                    broadcast_msg = broadcast_msg + ", "
                broadcast_msg = broadcast_msg + self.in_match[id_game][user]
                it += 1
            await self.broadcast_json(id_game,{"join": broadcast_msg })
            # await for messages and send messages
            while True and websocket.client_state == WebSocketState.CONNECTED:
                print("ENTRE")
                data = await websocket.receive_json()
                if data == {"connection": "close"} and user_name != list(self.in_match[id_game].keys())[0]:
                    remove_player(id_game, id_robot, user_name)
                    await self.disconnect(id_game, user_name, websocket)
                    await self.broadcast_json(id_game, {"leave": msg})
                    break
                else:
                    await self.send_personal_json({"Error": "No puedes abandonar la partida"}, websocket)
        except Exception or RuntimeError:
            if (websocket.client_state == WebSocketState.CONNECTED):
                await websocket.send_json({"status": "Cerrada - " + msg})
            try:
                if (user_name in list(self.active_connections[id_game].keys())):
                    await self.disconnect(id_game, user_name, websocket)
            except KeyError:
                print("Partida Eliminada")
            remove_player(id_game, id_robot, user_name)
            await self.broadcast_json(id_game, {"leave": msg})

    async def disconnect(self, id_game: int, name_player: int, websocket):
        socket_to_close = ""
        if websocket.client_state == WebSocketState.CONNECTED:
            socket_to_close = self.active_connections[id_game].get(name_player)
        self.active_connections[id_game].pop(name_player)
        self.in_match[id_game].pop(name_player)
        if self.active_connections[id_game] == {}:  # Empty game
            self.active_connections.pop(id_game)
            self.in_match.pop(id_game)
        await socket_to_close.close()

    async def send_personal_json(self, message, websocket: WebSocket):
        await websocket.send_json(message)
        return

    async def broadcast_text(self, id_game: int, message: str):
        game = self.active_connections.get(id_game)
        if game != None:
            for connection in game.values():
                await connection.send_text(message)
        return

    async def broadcast_json(self, id_game: int, message):
        game = self.active_connections.get(id_game)
        if game != None:
            for connection in game.values():
                await connection.send_json(message)
        return

    def exist_socket_of_player(self, id_game: int, name_player: int) -> bool:
        game = self.active_connections.get(id_game)
        if game != None:
            return True
        return False

    def get_all_connections(self):
        return self.active_connections

    def get_socket_player(self, id_game: int, name_player: int) -> WebSocket:
        game = self.active_connections.get(id_game)
        if game != None:
            player = name_player
            return name_player
