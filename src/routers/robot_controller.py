from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import UploadFile
from crud.robot_service import read_robots
from crud.robot_service import add_robot
from crud.robot_service import check_robot
from fastapi import Depends
from security.tokens import authorize_token
from db.database import database
from file_controller.store import save_file
from file_controller.store import generate_key

robot_end_points = APIRouter()


@robot_end_points.post("/Robots")
async def upload_robot(
    config: UploadFile, name: str, username: str = Depends(authorize_token)
):
    if check_robot(database, name, username):
        raise HTTPException(
            status_code=400, detail="ya existe un robot con el nomre" + name
        )
    else:
        add_robot(database, name, username)
        key = generate_key(name, username)
        save_file(config, key + ".py", "../robots_files/")
        return "robot agregado"


@robot_end_points.get("/Robots")
async def get_robots(username: str = Depends(authorize_token)):
    """Listar Robots

    Args:
        token (str): token

    Returns:
        str: Error
        List[Robots]: Lista de robots.
    """
    robots = read_robots(database, username)
    return robots

    # convertir robots en json
    # return robots
