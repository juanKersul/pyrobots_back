from datetime import datetime

# from types import NoneType
from pony.orm import db_session, commit, select, left_join
from schemas import imatch
from models.entities import Match, User, Robot
from crud.user_services import decode_JWT, encrypt_password, search_user_by_email
from routers.simulation_controller import game
from crud import simulation_service as sc
from crud.robot_service import get_file_by_id
from random import randint
import re


def is_email(user_crator: str):
    regex = (
        r"[a-zA-Z0-9_.-]+[^!#$%^&*()]@(?:gmail"
        r"|hotmail|yahoo|live|mi.unc|outlook)\.(?:com|es|edu.ar)"
    )
    result = isinstance(re.search(regex, user_crator), re.Match)
    return result


def is_username(user_creator: str):
    result = True
    if user_creator == "":
        resutl = False
    if " " in user_creator:
        result = False
    if len(user_creator) > 40:
        result = False
    return result


def find_by_username_or_email(user_creator: str):
    if is_email(user_creator):
        result = search_user_by_email(user_creator)
        if isinstance(result, NoneType):
            raise Exception
    elif is_username(user_creator):
        result = User[user_creator]
    return result


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


def parse_robots(robot_list: list):
    """Dado un arreglo de id de robots devuelve el comportamiento
    correspondiente a ese id segun el archivo .py

    Args:
        robot_list (list): Lista de valores enteros que se corresponden con
        los id de los robots en la partida

    Returns:
        robots (list): Lista de objetos cuyas clases están definidas en
        un archivo .py.
    """
    robots = []
    for x in robot_list:
        file = get_file_by_id(x)
        if "default1" in file:
            file = "default1.py"
        elif "default2" in file:
            file = "default2.py"

        filename = "routers/robots/" + file
        exec(
            open(filename).read(),
            globals(),
        )
        file = file.strip(".py")
        file = file.split("_")[0]
        klass = globals()[file]
        r = klass((randint(100, 800), randint(100, 800)), randint(0, 360))
        robots.append(r)
    return robots


def add_robot_attributes(
    n_games: int, n_rounds: int, robots: list, robot_id_list: list
):
    """Dada una lista de objetos de robots, ejecuta n_games cantidad de juegos
    con n_rounds rondas cada una, y los devuelve en un arreglo de arreglos

    Args:
        n_games (int): Cantidad de juegos a jugar en la partida
        n_rounds (int): Cantidad de rondas que cada juego va a tener
        robots (list): Lista de objetos que contiene comportamiento de los robots
        robot_id_list (list): Lista de los id de cada robot en partida

    Returns:
        outer_response (list): Arreglo de arreglos de arrreglos de objetos JSON
    """
    outer_response = []
    for i in range(n_games):
        outer_response.append(game(robots, n_rounds))
        for j in outer_response:
            for i in j:
                k = 0
                for j in i:
                    j["id"] = robot_id_list[k]
                    j["nombre"] = sc.get_robot_name(robot_id_list[k])
                    j["imagen"] = sc.get_robot_avatar(robot_id_list[k])
                    k += 1
    return outer_response


def games_last_round(outer_response: list):
    """Dado un arreglo de arreglos de arreglos de objetos JSON que representan
    la ejecucion de una partida devuelve el ultimo arreglo de objetos JSON de cada
    partida que representan la última ronda de la misma

    Args:
        outer_response (list): Arreglo de arreglos de arreglos de objetos JSON

    Returns:
        juego (list): Diccionario de valores que contiene la ultima ronda de
        cada juego.
    """
    final_round = []
    juego = {}
    contador = 0
    # Para cada partida
    for i in outer_response:
        contador += 1
        # Para rondas de partida
        for j in i:
            final_round.append(j)
        juego["Juego: " + str(contador)] = final_round[-1]
    return juego


def get_winners(juego: list):
    """Dado un diccionario de valores que contiene la ultima ronda de cada
    juego devuelve aquellos robots que aun estén vivos en la última ronda

    Args:
        juego (list): Diccionario de valores que contiene la ultima ronda de
        cada juego

    Returns:
        resultado: Diccionario que contiene los robots vivos al final de la
        ejecucion de cada juego
    """
    robots_sobrevivientes = []
    resultado = {}
    contador2 = 0
    for i in juego:
        contador2 += 1
        for j in juego[i]:
            if j["vida"] > 0:
                robots_sobrevivientes.append(j)
        resultado["Ganador/es juego: " + str(contador2)] = robots_sobrevivientes
        robots_sobrevivientes = []
    return resultado


def return_results(resultado: list):
    resultado2 = {}
    for i in resultado:
        for j in resultado[i]:
            resultado2[j["nombre"]] = 0
    for i in resultado:
        for j in resultado[i]:
            resultado2[j["nombre"]] += 1
    temp_value = 0
    ganador = {}
    for i in resultado2:
        if resultado2[i] > temp_value:
            temp_value = resultado2[i]
            ganador["ganador"] = i
    ganador["resultado"] = resultado2
    return ganador

@db_session
def delete_match(id_match: int):
    with db_session:
        try:
            Match[id_match].delete()
        except Exception as e:
            return str(e)