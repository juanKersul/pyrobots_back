from pony.orm import db_session
from pony.orm import commit
from pony.orm import rollback
from pony.orm import select
from pony.orm import ObjectNotFound
from pony.orm import OperationalError
from security.password import encrypt_password
from db.entities import Match
from db.entities import User
from db.entities import Robot


@db_session
def create_match(
    user_creator: str,
    max_players: int,
    password: str,
    n_matchs: int,
    n_rounds: int,
):
    """Crear Partida
    args:
        user_creator: nombre del usuario creador
        max_players: numero maximo de jugadores
        password: contraseña de la partida
        n_matchs: numero de partidas
        n_rounds: numero de rondas
    raises:
        OperationalError: fallo crear partida"""
    try:
        Match(
            max_players=abs(max_players),
            password=encrypt_password(password),
            n_matchs=min(abs(n_matchs), 200),
            n_rounds_matchs=min(abs(n_rounds), 10000),
            users={user_creator},
            user_creator=user_creator,
        )
        commit()
    except OperationalError("fallo crear partida"):
        rollback()
        raise


@db_session
def read_matchs():
    """Listar Partidas

    Args:
        token (str): token

    Returns:
        str: En caso de error
        List[Match]: Lista de partidas.
    """
    try:
        matchs = select(x for x in Match)
        return matchs
    except ObjectNotFound("fallo listar partidas"):
        raise


@db_session
def add_player(id_match: int, id_robot: int, username: str):
    """_summary_

    Args:
        id_match (int): _description_
        id_robot (int): _description_
        username (str): _description_

    Returns:
        _type_: _description_
    """
    try:
        match = Match[id_match]
        user = User[username]
        robot = Robot[id_robot]
        if (
            match.user_creator == user
            and len(match.robots_in_match) == 0
            and str(robot.name).split("_")[1] == username
        ):
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
    """
    Elimina un jugador de una partida.
    args:
        id_match: id de la partida
        id_robot: id del robot
        name_user: nombre del usuario
    raises:
        OperationalError: fallo eliminar jugador"""
    try:
        match = Match[id_match]
        user = User[name_user]
        in_match = match.robots_in_match
        in_match.remove(id_robot)
        match.robots_in_match = in_match
        match.users.remove(user)
        commit()
    except OperationalError("fallo eliminar jugador"):
        rollback()
        raise


@db_session
def delete_match(db, id_match: int):
    """
    Elimina una partida.
    args:
        id_match: id de la partida
    raises:
        OperationalError: fallo eliminar partida"""
    try:
        db.Match[id_match].delete()
        commit()
    except OperationalError("fallo eliminar partida"):
        rollback()
        raise
