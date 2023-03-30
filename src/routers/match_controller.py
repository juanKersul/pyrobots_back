from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from schemas import imatch
from crud import match_service
from pony.orm import db_session

from websockets2 import websocket_services


match_end_points = APIRouter()

manager = websocket_services.ConnectionManager()


@match_end_points.post("/match/add")
async def create_match(match: imatch.MatchCreate):
    msg = match_service.create_match(match)
    if "IntegrityError" in msg and "name" in msg:
        raise HTTPException(status_code=409, detail="El nombre de la partida ya existe")
    if "ObjectNotFound" in msg:
        raise HTTPException(status_code=400, detail="El usuario o email no existe")
    response = match_service.get_match_id(match.name)
    return {"id_match": response}


@match_end_points.post("/match/run")
async def start_match(id_match: int, token: str):
    robot_list = match_service.start_game(id_match, token)
    if "Status" in robot_list:
        return robot_list
    if "Token no valido" in robot_list:
        raise HTTPException(
            status_code=400,
            detail="Sesión expirada",
        )
    if "ObjectNotFound" in robot_list:
        raise HTTPException(
            status_code=400,
            detail="La cantidad de jugadores no coincide con los parámetros de la partida",
        )
    if "'>' not supported between instances of 'int' and 'str'" in robot_list:
        raise HTTPException(status_code=401, detail="No autorizado, debe loguearse")
    n_rounds = match_service.get_match_rounds(id_match)
    n_games = match_service.get_match_games(id_match)
    robots = match_service.parse_robots(robot_list)
    outer_response = match_service.add_robot_attributes(
        n_games, n_rounds, robots, robot_list
    )
    juego = match_service.games_last_round(outer_response)
    resultado = match_service.get_winners(juego)
    ganador = match_service.return_results(resultado)

    await manager.broadcast_json(id_match, {"status": "Iniciando partida"})
    await manager.broadcast_json(id_match, ganador)
    in_match = list(manager.active_connections[id_match].keys())
    in_match.reverse()
    for users in in_match:
        await manager.disconnect(
            id_match, users, manager.active_connections[id_match][users]
        )
    match_service.delete_match(id_match)
    return ganador


@match_end_points.websocket("/ws/match/{id_game}/{tkn}/{id_robot}")
async def join_match(websocket: WebSocket, id_game: int, tkn: str, id_robot: int):
    await manager.connect(websocket, id_game, tkn, id_robot)


@match_end_points.get("/matchs")
async def read_matchs(token: str):
    """Lista las partidas

    Args:
        token (str): recibe el token

    Returns:
        str: Error.
        List[Match]: Lista de partidas.
    """
    msg = match_service.read_matchs(token)
    if "'>' not supported between instances of 'int' and 'str'" in msg:
        raise HTTPException(status_code=401, detail="No autorizado, debe logearse")
    return msg
