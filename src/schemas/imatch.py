from typing import Set

from pydantic import BaseModel, validator
import re



class MatchBase(BaseModel):
    name: str
    max_players: int
    min_players: int
    password: str
    n_matchs: int
    n_rounds_matchs: int

    @validator("name")
    def name_validator(cls, name):
        regex = r"\s+"
        if name == "":
            raise ValueError("El nombre no puede ser vacío")
        if re.search(regex, name):
            raise ValueError("El nombre no puede contener caracteres vacíos")
        return name

    @validator("max_players")
    def max_players_validator(cls, max_players):
        if max_players == "":
            raise ValueError("Un campo obligatorio está vacío")
        if not isinstance(max_players, int):
            raise ValueError("El valor 'máximo de jugadores' debe ser un número")
        if not (2 <= max_players <= 4):
            raise ValueError("La cantidad de jugadores debe estar entre 2 y 4")
        return max_players

    @validator("min_players")
    def min_players_validator(cls, min_players):
        if min_players == "":
            raise ValueError("Un campo obligatorio está vacío")
        if not isinstance(min_players, int):
            raise ValueError("El valor 'mínimo de jugadores' debe ser un número")
        if not (2 <= min_players <= 4):
            raise ValueError("La cantidad de jugadores debe estar entre 2 y 4")
        return min_players

    @validator("n_matchs")
    def n_matchs_validator(cls, n_matchs):
        if n_matchs == "":
            raise ValueError("Un campo obligatorio está vacío")
        if not isinstance(n_matchs, int):
            raise ValueError("El valor 'número de juegos' debe ser un número")
        if not (1 <= n_matchs <= 200):
            raise ValueError("La cantidad de juegos debe estar entre 1 y 200")
        return n_matchs

    @validator("n_rounds_matchs")
    def n_rounds_matchs_validator(cls, n_rounds_matchs):
        if n_rounds_matchs == "":
            raise ValueError("Un campo obligatorio está vacío")
        if not isinstance(n_rounds_matchs, int):
            raise ValueError("El valor 'número de rounds' debe ser un número")
        if not (2 <= n_rounds_matchs <= 10000):
            raise ValueError("La cantidad de rondas debe estar entre 2 y 10.000")
        return n_rounds_matchs


class MatchCreate(MatchBase):
    user_creator: str
    token: str

    class Config:
        orm_mode = True


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True
