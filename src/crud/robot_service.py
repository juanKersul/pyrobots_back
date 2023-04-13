from pony.orm import db_session
from pony.orm import commit
from pony.orm import rollback
from pony.orm import select
from pony.orm import OrmError
from db.entities import Robot
from src.exceptions import OperationalError
from src.exceptions import ObjectNotFound


@db_session
def add_robot(robot_name: str, username: str):
    """Agregar robot a la base de datos.
    Args:
        robot_name (str): Nombre del robot.
        username (str): Nombre de usuario o email.
    """
    try:
        Robot(
            name=robot_name,
            matchs_played=0,
            matchs_won=0,
            avg_life_time=0.0,
            user_owner=username,
        )
        commit()
    except OrmError:
        rollback()
        raise OperationalError("No se pudo agregar el robot")


@db_session
def read_robots(username: str):
    """Listar robots, consulta a la base de datos.
    Args:
        username (str): nombre del usuario.
    Returns:
        List[Robot]: Lista de robots.
    Raises:
        ObjectNotFound: No se encontraron robots.
        OperationalError: No se pudo leer la base de datos.
    """
    try:
        robots = select(x for x in Robot if x.user_owner.username == username)
    except OrmError:
        raise OperationalError("No se pudo leer la base de datos")
    if robots is None:
        raise ObjectNotFound("No se encontraron robots")
    else:
        return robots


@db_session
def check_robot_name(robot_name: str, username: str):
    """Verifica si el nombre del robot existe.
    Args:
        robot_name (str): Nombre del robot.
    Returns:
        bool: True si existe, False si no existe.
    """
    try:
        return Robot.exists(name=robot_name, user_owner=username)
    except OrmError:
        raise OperationalError("No se pudo leer la base de datos")
