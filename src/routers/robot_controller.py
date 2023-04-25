from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import UploadFile
from crud import robot_service
from crud.robot_service import add_robot
import base64
from fastapi import Depends
from routers.session_controller import authorization

robot_end_points = APIRouter()


@robot_end_points.post("/Robot")
async def upload_robot(
    config: UploadFile, name: str, username: str = Depends(authorization)
):
    """Cargar Robot

    Args:
        config (UploadFile): archivo del robot.
        avatar (UploadFile): imagen del robot.
        name (str): nombre del robot.
        tkn (str): token.
        username (str): nombre de usuario.

    Raises:
        HTTPException: 409: El robot ya existe.
        HTTPException: 400: El usuario no existe.
        HTTPException: 422: El nombre del Robot con el archivo no se corresponden.
        HTTPException: 440: El token no es correcto o está expirado.

    Returns:
        _type_: _description_
    """
    no_avatar = True
    if avatar != None:
        avatar_name = "P" + avatar.filename
        no_avatar = False
    else:
        avatar_name = "default.jpeg"
    msg = add_robot(config, avatar_name, name, tkn)
    # El robot ya existe
    if "ya existe" in msg:
        raise HTTPException(status_code=409, detail=msg)
    # Los nombres para el robot no se corresponden
    if "requisitos" in msg:
        raise HTTPException(status_code=422, detail=msg)
    # Token invalido o expirado
    if "Token" in msg:
        raise HTTPException(status_code=440, detail="Sesión expirada")
    # Tomamos el nombre del usuario y el nombre del archivo
    username = msg.split(":")[1]
    avatar_name = msg.split(":")[2]
    msg = msg.split(":")[0]
    store_config(config, username)
    if not no_avatar:
        avatar.filename = avatar_name
        store_avatar(avatar)
    return {"msg": msg}


@robot_end_points.get("/Robots")
def read_robots(token: str = Depends(authorization)):
    """Listar Robots

    Args:
        token (str): token

    Returns:
        str: Error
        List[Robots]: Lista de robots.
    """
    msg = robot_service.read_robots(token)
    if "'>' not supported between instances of 'int' and 'str'" in msg:
        raise HTTPException(status_code=401, detail="No autorizado, debe logearse")
    return msg
