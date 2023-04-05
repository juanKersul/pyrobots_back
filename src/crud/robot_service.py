from pony.orm import db_session
from pony.orm import commit
from pony.orm import rollback
from pony.orm import select
from pony.orm import ObjectNotFound
from pony.orm import OperationalError
from db.entities import Robot


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
    except OperationalError:
        rollback()
        raise


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
    except OperationalError("no se pudo leer la base de datos"):
        raise
    if robots is None:
        raise ObjectNotFound("No se encontraron robots")
    else:
        return robots

