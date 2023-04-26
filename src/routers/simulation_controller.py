from fastapi import APIRouter
from fastapi import Depends
from security.tokens import authorize_token
from crud.robot_service import check_robot
from fastapi import HTTPException
from file_controller.store import generate_key
from file_controller.execute import execute_file
from random import randint

simulation_end_points = APIRouter()


@simulation_end_points.get("/Simulation")
async def run_simulation(
    robots: frozenset, rounds: int, games: int, username: str = Depends(authorize_token)
):
    for robot in robots:
        if not check_robot(robot, username):
            raise HTTPException(status_code=404, detail="Robot not found")
    robot_object_list = []
    for robot in robots:
        filename = generate_key(robot, username)
        path = "../robots_files/" + filename + ".py"
        robot_class = execute_file(path, filename)
        robot_object = robot_class(
            (randint(100, 800), randint(100, 800)), randint(0, 360)
        )
        robot_object_list.append(robot_object)
    results_list = []
    for i in range(games):
        game = Game(robot_object_list, rounds)
        game.run()
        results = game.get_results()
        results_list.append(results)
    return results_list

    
    # CREAR UN OBJETO GAME
    # outer_response = game(robots, simulation.n_rounds_simulations)
    # EJECUTAR GAME CON LOS PARAMETROS
    # GENERAR RESPUESTA
