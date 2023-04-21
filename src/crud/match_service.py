from pony.orm import db_session
from pony.orm import commit
from pony.orm import rollback
from pony.orm import select
from pony.orm import OrmError
from exceptions.classes import OperationalError


@db_session
def create_match(
    db,
    user_creator: str,
    max_players: int,
    password: str,
    max_matches: int,
    max_rounds: int,
) -> int:
    """_summary_

    Args:
        user_creator (str): user that creates the match
        max_players (int): max players in match
        password (str): password of match
        max_matches (int): max matches in match
        max_rounds (int): max rounds in match

    Raises:
        ObjectNotFound: user_creator not found
        OperationalError: failed to search user_creator
        OperationalError: failed to create match
    """
    try:
        user = db.User[user_creator]
    except OrmError as e:
        raise OperationalError("failed to search user", e)
    try:
        new_match = db.Match(
            max_players=max_players,
            password=password,
            n_matches=max_matches,
            n_rounds=max_rounds,
            user_creator=user,
            active=False,
        )
        commit()
        return new_match.get_pk()
    except OrmError as e:
        rollback()
        raise OperationalError("failed to create match", e)


@db_session
def read_matchs(db):
    """Listar Partidas

    Args:
        token (str): token

    Returns:
        str: En caso de error
        List[Match]: Lista de partidas.
    """
    try:
        return select(x for x in db.Match if db.Match.active is True)
    except OrmError as e:
        raise OperationalError("failed to read matches", e)


@db_session
def add_player(db, id_match: int, robot_name: str, user_name: str):
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
        match = db.Match[id_match]
    except OrmError as e:
        raise OperationalError("fallo buscar jugador", e)
    try:
        user = db.User[user_name]
    except OrmError as e:
        raise OperationalError("fallo buscar usuario", e)
    try:
        robot = db.Robot[robot_name, user_name]
    except OrmError as e:
        raise OperationalError("fallo buscar robot", e)

    if len(match.robots_in_match) < match.max_players:
        match.robots_in_match.add(robot)
        match.users.add(user)
        commit()
    else:
        raise OperationalError("partida llena")


@db_session
def remove_player(db, id_match: int, robot_name: str, user_name: str):
    """
    Elimina un jugador de una partida.
    args:
        id_match: id de la partida
        id_robot: id del robot
        name_user: nombre del usuario
    raises:
        OperationalError: fallo eliminar jugador"""
    try:
        match = db.Match[id_match]
    except OrmError as e:
        raise OperationalError("fallo buscar partida", e)
    try:
        user = db.User[user_name]
    except OrmError as e:
        raise OperationalError("fallo buscar usuario", e)
    try:
        robot = db.Robot[robot_name, user_name]
    except OrmError as e:
        raise OperationalError("fallo buscar robot", e)
    try:
        match.robots_in_match.remove(robot)
        match.users.remove(user)
        commit()
    except OrmError as e:
        rollback()
        raise OperationalError("fallo eliminar jugador", e)


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
    except OrmError as e:
        rollback()
        raise OperationalError("fallo eliminar partida", e)


@db_session
def check_match(db, id_match: int):
    """
    Comprueba si existe una partida.
    args:
        id_match: id de la partida
    returns:
        bool: True si existe, False si no existe.
    """
    try:
        return db.Match.exists(id=id_match)
    except OrmError as e:
        raise OperationalError("fallo buscar partida", e)


@db_session
def active_match(db, id_match: int):
    """
    Activa una partida.
    args:
        id_match: id de la partida
    raises:
        OperationalError: fallo activar partida
    """
    try:
        match = db.Match[id_match]
        match.active = True
        commit()
    except OrmError as e:
        rollback()
        raise OperationalError("fallo activar partida", e)
