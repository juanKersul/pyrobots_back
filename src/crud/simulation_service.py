from pony.orm import db_session, commit, select

from db.entities import Match, User, Robot


@db_session
def check_robot(id):
    """Chequea que un robot exista en la base de datos.

    Args:
        id (Any): id del robot a chequear.

    Returns:
        Any: ??
    """
    return Robot.exists(id=id)


@db_session
def check_user(username):
    """Chequea que un usuario exista en la bd.

    Args:
        username (Any): Nombre del usuario a chequear en la bd.

    Returns:
        Any: ??
    """
    return User.exists(username=username)


@db_session
def get_robot_name(id_robot):
    robots = select(r.name for r in Robot if r.id == id_robot)
    for i in robots:
        return i


@db_session
def get_robot_avatar(id_robot):
    robots = select(r.avatar for r in Robot if r.id == id_robot)
    for i in robots:
        return i


@db_session
def get_robot_avatar(id_robot):
    robots = select(r.avatar for r in Robot if r.id == id_robot)
    for i in robots:
        return i


@db_session
def get_robot_id(robot_name):
    robots = select(r.id for r in Robot if r.name == robot_name)
    for i in robots:
        return i
