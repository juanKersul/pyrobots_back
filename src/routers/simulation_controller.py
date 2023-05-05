from fastapi import APIRouter
from fastapi import Depends
from security.tokens import authorize_token
from crud.robot_service import check_robot
from fastapi import HTTPException
from file_controller.execute import execute_file
from game.game import BaseGame
from db.database import database
from schemas.simulation import Simulation
from game.Robot import Py_Robot

simulation_end_points = APIRouter()


@simulation_end_points.post("/Simulation")
async def run_simulation(params: Simulation, username: str = Depends(authorize_token)):
    # check if robots exist
    for robot_name in params.robots:
        if not check_robot(database, robot_name, username):
            raise HTTPException(status_code=404, detail="Robot not found")
    robot_object_list = []
    # generate robot objects
    for robot_name in params.robots:
        path = "../robots_files/" + username + "/" + robot_name + ".py"
        command_object = execute_file(path, robot_name)
        robot_object = Py_Robot(robot_name, command_object)
        robot_object_list.append(robot_object)
    # run game
    game = BaseGame(robot_object_list)
    game.run(params.rounds)
    results = game.get_results()
    return results
