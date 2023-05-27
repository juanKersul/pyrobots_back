from fastapi import APIRouter
from fastapi import HTTPException
from models.crud.match_service import create_match
from models.crud.match_service import add_player
from models.crud.user_services import check_user
from models.crud.robot_service import check_robot
from models.crud.match_service import read_matchs
from models.crud.match_service import check_match
from models.crud.match_service import get_match
from models.crud.match_service import check_match_is_full
from fastapi import Depends
from controllers.security.tokens import authorize_token
from models.db.database import database
from controllers.websockets2.websocket_services import server
from controllers.file_controller.execute import execute_file
from controllers.game.Robot import Py_Robot
from controllers.game.game import BaseGame

match_end_points = APIRouter()


@match_end_points.post("/match")
async def add_match(
    robot: str,
    max_players: int,
    password: str,
    max_rounds: int,
    username: str = Depends(authorize_token),
):
    if check_user(database, username):
        if check_robot(database, robot, username):
            key = server.new_sub()
            match = create_match(
                database, username, max_players, password, max_rounds, key
            )
            add_player(database, match, robot, username)
            return {"id_match": match, "key": key}
        else:
            raise HTTPException(
                status_code=400,
                detail="Robot no encontrado",
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Usuario no encontrado",
        )


@match_end_points.put("/match/{id_match}/join")
async def join_match(
    robot: str, id_match: int, username: str = Depends(authorize_token)
):
    if check_user(database, username):
        if check_robot(database, robot, username):
            if check_match(database, id_match):
                if not check_match_is_full(database, id_match):
                    key = get_match(database, id_match)["key"]
                    add_player(database, id_match, robot, username)
                    await server.send_message_to_subscribers(
                        key, username + " se ha unido"
                    )
                    return {"key": key}

                else:
                    raise HTTPException(
                        status_code=400,
                        detail="Partida llena",
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Partida no encontrada",
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Robot no encontrado",
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Usuario no encontrado",
        )


@match_end_points.get("/match/{id_match}/start")
async def start_match(id_match: int, username: str = Depends(authorize_token)):
    if check_user(database, username):
        if check_match(database, id_match):
            match = get_match(database, id_match)
            if match["user_creator"] == username:
                robot_object_list = []
                for robots in match["robots_in_match"]:
                    path = "../robots_files/" + robots[1] + "/" + robots[0] + ".py"
                    print(path)
                    command_object = execute_file(path, robots[0])
                    robot_object = Py_Robot(robots[1], command_object)
                    robot_object_list.append(robot_object)
                game = BaseGame(robot_object_list)
                game.run(match["n_rounds"])
                results = game.get_results()
                await server.send_message_to_subscribers(results, match["key"])
                return "partida iniciada con exito"
            else:
                raise HTTPException(
                    status_code=400,
                    detail="no eres el creador de la partida",
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Partida no encontrada",
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Usuario no encontrado",
        )


@match_end_points.get("/matchs")
async def get_matchs(username: str = Depends(authorize_token)):
    if check_user(database, username):
        return read_matchs(database)
    else:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
