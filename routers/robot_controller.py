from fastapi import APIRouter, HTTPException, UploadFile, File
from crud import robot_service
from crud.robot_service import add_robot,get_image_name
import shutil
from typing import Optional
import base64
robot_end_points = APIRouter()


def store_config(file: UploadFile, owner: str):
    file.file.seek(0)
    new_filename = file.filename.replace(".py", "_" + owner + ".py")
    with open("routers/robots/" + new_filename, "wb+") as upload_folder:
        shutil.copyfileobj(file.file, upload_folder)


def store_avatar(file: UploadFile):
    file.file.seek(0)
    with open("routers/robots/avatars/" + file.filename, "wb+") as upload_folder:
        shutil.copyfileobj(file.file, upload_folder)


@robot_end_points.post("/upload/robot")
async def robot_upload(
    *, config: UploadFile, avatar: Optional[UploadFile] = File(None), name: str, tkn: str):
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


@robot_end_points.get("/robots")
def read_robots(token: str):
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

@robot_end_points.get("/image")
def get_image(token,robot_id):
    image_name = get_image_name(token,robot_id)
    path = "routers/robots/avatars/"+image_name
    with open(path, 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image