from pony.orm import db_session
from pony.orm import commit
from pony.orm import rollback
from pony.orm import select
from exceptions.classes import OperationalError
from pony.orm import OrmError


@db_session
def add_robot(db, robot_name: str, username: str):
    """Agregar robot a la base de datos.
    Args:
        robot_name (str): Nombre del robot.
        username (str): Nombre de usuario o email.
    """
    try:
        db.Robot(
            name=robot_name,
            matchs_played=0,
            matchs_won=0,
            avg_life_time=0.0,
            user_owner=username,
        )
        commit()
    except OrmError as e:
        rollback()
        raise OperationalError("No se pudo agregar el robot", e)


@db_session
def read_robots(db, username: str):
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
        return select(x for x in db.Robot if x.user_owner.username == username)
    except OrmError as e:
        raise OperationalError("No se pudo leer la base de datos", e)


@db_session
def check_robot(db, robot_name: str, username: str):
    """Verifica si el nombre del robot existe.
    Args:
        robot_name (str): Nombre del robot.
    Returns:
        bool: True si existe, False si no existe.
    """
    try:
        return db.Robot.exists(name=robot_name, user_owner=username)
    except OrmError as e:
        raise OperationalError("No se pudo verificar el nombre del robot", e)


@db_session
def read_robot(db, robot_name: str, username: str):
    """Lee un robot de la base de datos.
    Args:
        robot_name (str): Nombre del robot.
        username (str): Nombre de usuario o email.
    Returns:"""
    try:
        return db.Robot[robot_name, username]
    except OrmError as e:
        raise OperationalError("No se pudo leer el robot", e)
