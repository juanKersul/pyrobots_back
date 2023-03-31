from pony.orm import db_session, commit, select
from schemas import irobot


@db_session
def add_robot(avatar_file: str, robot_name: str):
    """Agregar robot a la base de datos.
    Args:
        config_file (UploadFile): Archivo '.py' del robot.
        avatar_file (str): Imagen del robot.
        robot_name (str): Nombre del robot.
        user_token (str): Token.
        username (str): Nombre de usuario o email.

    Returns:
        str: Mensaje de retorno.
    """
    username = ""
    with db_session:
        try:
            if avatar_file != "default.jpeg":
                avatar_file = avatar_file[1:].split(".")
                avatar_file[0] = username + "_" + robot_name + "."
                avatar_file = "".join(avatar_file)
            Robot(
                name=robot_name + "_" + username,
                avatar=avatar_file,
                matchs_pleyed=0,
                matchs_won=0,
                avg_life_time=0,
                user_owner=username,
            )
            commit()
        except Exception as e:
            return str("El robot ya existe")
        return "Robot agregado con exito:" + username + ":" + avatar_file


@db_session
def read_robots(username: str):
    """Listar robots, consulta a la base de datos.
    Args:
        token (str): token.
    Returns:
        str: En caso de error.
        List[Robot]: Lista de robots.
    """
    with db_session:
        try:
            robots = select(x for x in Robot if x.user_owner.username == username)
            result = [irobot.Robot.from_orm(r) for r in robots]
            commit()
        except Exception as e:
            return str(e)
        return result
