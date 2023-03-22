from datetime import datetime

# from types import NoneType
from pony.orm import db_session, commit, select
from schemas import imatch
from db.entities import Match, User, Robot
from crud.user_services import decode_JWT, encrypt_password
from routers.simulation_controller import game
from crud import simulation_service as sc
from crud.robot_service import get_file_by_id
from random import randint

@db_session
def create_match(match: imatch.MatchCreate):
    with db_session:
        decode_token = decode_JWT(match.token)
        if decode_token["expiry"] > str(datetime.now()):
            try:
                creator_aux = find_by_username_or_email(match.user_creator)
            except Exception as e:
                return "ObjectNotFound"
            try:
                Match(
                    name=match.name,
                    max_players=abs(match.max_players),
                    min_players=abs(match.min_players),
                    password=encrypt_password(match.password),
                    n_matchs=min(abs(match.n_matchs), 200),
                    n_rounds_matchs=min(abs(match.n_rounds_matchs), 10000),
                    users={
                        creator_aux,
                    },
                    user_creator=creator_aux,
                )
                commit()
            except Exception as e:
                return str(e)
        else:
            return "Token no válido"
        return "added"


@db_session
def read_matchs(token: str):
    """Listar Partidas

    Args:
        token (str): token

    Returns:
        str: En caso de error
        List[Match]: Lista de partidas.
    """
    with db_session:
        decode_token = decode_JWT(token)
        try:
            if decode_token["expiry"] > str(datetime.now()):
                matchs = select(x for x in Match)[:]
                result = [
                    {
                        "id": p.id,
                        "name": p.name,
                        "max_players": p.max_players,
                        "min_players": p.min_players,
                        "n_matchs": p.n_matchs,
                        "n_rounds_matchs": p.n_rounds_matchs,
                        "user_creator": p.user_creator.username
                        + ":"
                        + p.user_creator.email,
                    }
                    for p in matchs
                ]
                commit()
            else:
                result = "Token no válido"
        except Exception as e:
            return str(e)
        return result


@db_session
def read_match(id_match: int):
    with db_session:
        try:
            match = Match[id_match]
            result = imatch.Match.from_orm(match)
            commit()
        except Exception as e:
            return str(e)
        return result


@db_session
def get_match_id(match_name: str):
    result = select(m.id for m in Match if m.name == match_name)
    for i in result:
        return i


@db_session
def get_match_max_players(match_id: int):
    query = select(m.max_players for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def get_match_min_players(match_id: int):
    query = select(m.min_players for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def get_match_rounds(match_id: int):
    query = select(m.n_rounds_matchs for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def get_match_games(match_id: int):
    query = select(m.n_matchs for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def read_match_players(id_match: int):
    str_result = []
    with db_session:
        result = select(m.users for m in Match if m.id == id_match)
        for i in result:
            str_result.append(i.username)
        return str_result


@db_session
def read_player_in_game(username: str, id_match: int):
    result = select(m.users for m in Match if m.id == id_match)

    return username in result


@db_session
def add_player(id_match: int, tkn: str, id_robot: int):
    result = ""
    with db_session:
        decode_token = decode_JWT(tkn)
        error = ""
        username = decode_token["userID"]
        if decode_token["expiry"] == 0:
            return "Token no valido"
        if str(decode_token["expiry"]) < str(datetime.now()):
            return "Token no valido"
        try:
            match = Match[id_match]
            user = User[username]
            robot = Robot[id_robot]
            if match.user_creator == user and len(match.robots_in_match) == 0 and str(robot.name).split("_")[1] == username:
                list_robots = match.robots_in_match
                list_robots.append(id_robot)
                match.robots_in_match = list_robots
                return str(username) + ":" + str(robot.name).split("_")[0]
            if len(match.users) == match.max_players:
                error = "La partida esta llena"
            elif str(robot.name).split("_")[1] != username:
                error = "El robot no pertenece al usuario"
            elif user in match.users:
                error = "El usuario ya esta en la partida"
        except Exception as e:
            if "Match" in str(e):
                error = "La partida no existe"
            elif "User" in str(e):
                error = "El usuario no existe"
            elif "Robot" in str(e):
                error = "El robot no existe"
            return error
        if error == "":
            match.users.add(user)
            list_robots = match.robots_in_match
            list_robots.append(id_robot)
            match.robots_in_match = list_robots
            result = str(username) + ":" + str(robot.name).split("_")[0]
        else:
            result = error
    return result


@db_session
def remove_player(id_match: int, id_robot: int, name_user: str):
    with db_session:
        try:
            result = "Dejo la partida"
            match = Match[id_match]
            user = User[name_user]
            in_match = match.robots_in_match
            in_match.remove(id_robot)
            match.robots_in_match = in_match
            match.users.remove(user)
        except Exception as e:
            error = ""
            if "Match" in str(e):
                error = "La partida no existe"
            elif "User" in str(e):
                error = "El usuario no existe"
            return error
        return result


@db_session
def start_game(id_match: int, token: str):
    with db_session:
        decode_token = decode_JWT(token)
        name_user = decode_token["userID"]
        try:
            if decode_token["expiry"] == 0:
                return "Token no valido"
            if str(decode_token["expiry"]) < str(datetime.now()):
                return "Token no valido"
            try:
                msg = ""
                match = Match[id_match]
                user = User[name_user]
                if not user.username == match.user_creator.username:
                    msg = {"Status": "No es el creador de la partida"}
                    return msg
                match_robots = match.robots_in_match
                if (len(match_robots) < get_match_min_players(id_match)) or (
                    len(match_robots) > get_match_max_players(id_match)
                ):
                    msg = {"ObjectNotFound"}
                    return msg
            except Exception as e:
                error = ""
                if "Match" in str(e):
                    error = {"Status": "La partida no existe"}
                elif "User" in str(e):
                    error = {"Status": "El usuario no existe"}
                return error
        except Exception as e:
            return str(e)
    return list(match_robots)

@db_session
def delete_match(id_match: int):
    with db_session:
        try:
            Match[id_match].delete()
        except Exception as e:
            return str(e)