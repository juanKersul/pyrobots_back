from typing import Set

from pydantic import BaseModel, validator
import re

from crud import simulation_service as sc


class SimulationBase(BaseModel):
    id_robot: str
    n_rounds_simulations: int

    @validator("id_robot")
    def id_robot_validator(cls, id_robot):
        id_robot_parsed = id_robot.split(",")
        regex = r"\s+"
        cant_robots = len(id_robot_parsed)
        if cant_robots > 4 or cant_robots < 2:
            raise ValueError("El valor debe estar entre 2 y 4")
        if not isinstance(id_robot, str):
            raise ValueError("El valor 'id de robots' debe ser un string")
        if re.search(regex, id_robot):
            raise ValueError("La lista de robots no puede contener caracteres vacíos")
        for i in id_robot_parsed:
            if not sc.check_robot(i):
                raise ValueError("El robot " + i + " no existe")
        return id_robot

    @validator("n_rounds_simulations")
    def n_rounds_simulations_validator(cls, n_rounds_simulations):
        if not isinstance(n_rounds_simulations, int):
            raise ValueError("El valor 'número de rounds' debe ser un número")
        if not (2 <= n_rounds_simulations <= 10000):
            raise ValueError("El valor debe estar entre 2 y 10.000")
        return n_rounds_simulations


class SimulationCreate(SimulationBase):
    user_creator: str
    token: str

    @validator("user_creator")
    def user_creator_validator(cls, user_creator):
        if not isinstance(user_creator, str):
            raise ValueError("El valor 'usuario creador' debe ser un string")
        if not sc.check_user(user_creator):
            raise ValueError("El usuario no existe")
        return user_creator
