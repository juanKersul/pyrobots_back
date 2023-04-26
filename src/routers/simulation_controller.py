from fastapi import APIRouter
from crud import robot_service as sc
from game.robot_class import Robot
from random import randint
from fastapi import Depends
from security.tokens import authorize_token

simulation_end_points = APIRouter()


@simulation_end_points.get("/Simulation")
async def run_simulation(
    robots: frozenset,
    rounds: int,
    games: int,
    username: str = Depends(authorize_token)
):
    for robot in robots:
        filename = generate_key(robot, username) + ".py"
        try:
            ## EXECUTE FILE WITH PYTHON
                #exec(
                #    open(filename).read(),
                #    globals(),
                #)
                #file = file.strip(".py")
                #klass = globals()[file]
            #INICIALIZAR LA CLASE    
                #r = klass((randint(100, 800), randint(100, 800)), randint(0, 360))
            #METER EL OBJETO EN UNA LISTA
            #robots.append(r)

    # for i in range(simulation.n_rounds_simulations):
    outer_response = game(robots, simulation.n_rounds_simulations)
    for i in outer_response:
        k = 0
        for j in i:
            j["id"] = id_robot_parsed[k]
            j["nombre"] = sc.get_robot(id_robot_parsed[k])
            k += 1
    return outer_response
