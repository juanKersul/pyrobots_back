from pony.orm import db_session
from pony.orm import commit
from pony.orm import select
from exceptions.classes import OperationalError
from exceptions.classes import ObjectNotFound
from db.database import database
db = database


@db_session
def add_robot(robot_name: str, username: str):
    """Agregar robot a la base de datos.
    Args:
        robot_name (str): Nombre del robot.
        username (str): Nombre de usuario o email.
    """
    if db.Robot.exists(name=robot_name, user_owner=username):
        raise OperationalError("El robot ya existe")
    if db.User.exists(name=robot_name) is False:
        raise OperationalError("El usuario no existe")
    db.Robot(
        name=robot_name,
        matchs_played=0,
        matchs_won=0,
        avg_life_time=0.0,
        user_owner=username,
    )
    commit()


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
    return select(x for x in db.Robot if x.user_owner.username == username)


@db_session
def check_robot(robot_name: str, username: str):
    """Verifica si el nombre del robot existe.
    Args:
        robot_name (str): Nombre del robot.
    Returns:
        bool: True si existe, False si no existe.
    """
    return db.Robot.exists(name=robot_name, user_owner=username)


@db_session
def read_robot(robot_name: str, username: str):
    """Lee un robot de la base de datos.
    Args:
        robot_name (str): Nombre del robot.
        username (str): Nombre de usuario o email.
    Returns: """
    if db.Robot.exists(name=robot_name, user_owner=username) is False:
        raise ObjectNotFound("El robot no existe")
    else:
        return db.Robot[robot_name, username]
