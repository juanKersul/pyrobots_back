from fastapi import APIRouter
from schemas import isim
from crud import simulation_service as sc
from routers.robot.robot_class import Robot
from routers.game.game import inflingir_danio, avanzar_ronda
from crud.robot_service import get_file_by_id
from pathlib import Path
from random import randint

simulation_end_points = APIRouter()


def game(robots:list, rounds):
    """Ejecuta un juego

    Args:
        robots (list): Lista de robots de la simulación
        rounds (int): Cantidad de rondas del juego

    Returns:
        List[Any]: Lista de Rondas, un juego.
    """
    results_by_robots = []
    for robot in robots:
        if robot != None:
            try:
                robot.initialize()
            except:
                pass
    for i in range(rounds):
        results_by_robots.append(avanzar_ronda(robots))
    return results_by_robots


@simulation_end_points.post("/simulation/add")
async def create_simulation(simulation: isim.SimulationCreate):
    """Crea una simulación.

    Args:
        simulation (isim.SimulationCreate): Simulación con todos sus campos.

    Returns:
        List[Any]: Lista con rondas.
    """
    id_robot_parsed = simulation.id_robot.split(",")
    outer_response = []
    robots = []
    for x in id_robot_parsed:
        file = get_file_by_id(x)
        if(("default1" in file)):
            file = "default1.py"
        elif("default2" in file):
            file = "default2.py"
        
        filename = (
            "routers/robots/"
            + file
        )
        try:
            exec(
                open(filename).read(),
                globals(),
            )
            file = file.strip(".py")
            file = file.split("_")[0]
            klass = globals()[file]
            r = klass((randint(100, 800), randint(100, 800)), randint(0, 360))
            robots.append(r)
        except:
            r = Robot((randint(100, 800), randint(100, 800)), randint(0, 360))
            r.current_damage = 0
            robots.append(r)

    # for i in range(simulation.n_rounds_simulations):
    outer_response = game(robots,simulation.n_rounds_simulations)
    for i in outer_response:
        k = 0
        for j in i:
            j["id"] = id_robot_parsed[k]
            j["nombre"] = sc.get_robot_name(id_robot_parsed[k])
            k += 1
    return outer_response
