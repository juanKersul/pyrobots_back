from pony.orm import db_session
from pony.orm import commit
from pony.orm import rollback
from pony.orm import select
from pony.orm import OrmError
from src.exceptions import OperationalError
from src.exceptions import ObjectNotFound
from db.entities import Match
from db.entities import User
from db.entities import Robot


@db_session
def create_match(
    user_creator: str,
    max_players: int,
    n_password: str,
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
            password=n_password,
            n_matchs=min(abs(n_matchs), 200),
            n_rounds_matchs=min(abs(n_rounds), 10000),
            users={user_creator},
            user_creator=user_creator,
        )
        commit()
    except OrmError:
        rollback()
        raise OperationalError("fallo crear partida")


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
    except OrmError:
        raise OperationalError("fallo listar partidas")


@db_session
def add_player(id_match: int, id_robot: int, username: str):
    """
    Añade un jugador a una partida.
    args:
        id_match: id de la partida
        id_robot: id del robot
        username: nombre del usuario
    raises:
        OperationalError: fallo añadir jugador
        OperationalError: partida llena
    """
    try:
        match = Match[id_match]
    except OrmError:
        raise ObjectNotFound("fallo leer partida")
    try:
        user = User[username]
    except OrmError:
        raise ObjectNotFound("fallo leer usuario")
    try:
        robot = Robot[id_robot]
    except OrmError:
        raise ObjectNotFound("fallo leer robot")
    try:
        match.robots_in_match.add(robot)
        match.users.add(user)
        commit()
    except OrmError:
        rollback()
        raise OperationalError("fallo añadir jugador")


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
    except OrmError:
        raise ObjectNotFound("fallo leer partida")
    try:
        user = User[name_user]
    except OrmError:
        raise ObjectNotFound("fallo leer usuario")
    try:
        robot = Robot[id_robot]
    except OrmError:
        raise ObjectNotFound("fallo leer robot")
    try:
        match.robots_in_match.remove(robot)
        match.users.remove(user)
        commit()
    except OperationalError("fallo eliminar jugador"):
        rollback()
        raise


@db_session
def delete_match(id_match: int):
    """
    Elimina una partida.
    args:
        id_match: id de la partida
    raises:
        OperationalError: fallo eliminar partida"""
    try:
        Match[id_match].delete()
        commit()
    except OperationalError("fallo eliminar partida"):
        rollback()
        raise


@db_session
def check_match(id_match: int):
    """
    Comprueba si existe una partida.
    args:
        id_match: id de la partida
    returns:
        bool: True si existe, False si no existe.
    """
    try:
        return Match.exists(id=id_match)
    except OrmError:
        raise OperationalError("fallo comprobar partida")
