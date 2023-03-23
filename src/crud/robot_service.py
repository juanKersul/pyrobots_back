from pony.orm import db_session, commit, select
from db.entities import Robot
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


@db_session
def get_file_by_id(rob_id: int):
    """Obtener un archivo por su id

    Args:
        rob_id (int): id del archivo

    Returns:
        Any: Nombre del archivo del robot.
    """
    with db_session:
        robot = Robot[rob_id]
        filename = robot.name + ".py"
        return filename


@db_session
def add_default_robot(username: str):
    """Agregar robot por defecto.
    Args:
        username (str): Usuario al que agregar robot por defecto.
    """
    with db_session:
        Robot(
            name="default1" + "_" + username,
            matchs_pleyed=0,
            matchs_won=0,
            avg_life_time=0,
            user_owner=username,
            avatar="default.jpeg",
        )
        commit()
        Robot(
            name="default2" + "_" + username,
            matchs_pleyed=0,
            matchs_won=0,
            avg_life_time=0,
            user_owner=username,
            avatar="default.jpeg",
        )
        commit()


@db_session
def get_image_name(username, id):
    with db_session:
        try:
            res = Robot[id]
            if res.user_owner.username == username:
                return res.avatar
            else:
                return "default.jpeg"
        except:
            return "default.jpeg"
