from pydantic import BaseModel, validator


class Simulation(BaseModel):
    robots: list[str]
    rounds: int

    @validator("robots")
    def robots_validator(cls, robots):
        if len(robots) < 2:
            raise ValueError("Se necesitan al menos 2 robots para jugar")
        if len(robots) > 4:
            raise ValueError("Se necesitan como maximo 4 robots para jugar")
        return robots

    @validator("rounds")
    def rounds_validator(cls, rounds):
        if rounds < 1:
            raise ValueError("Se necesita al menos 1 ronda para jugar")
        if rounds > 100:
            raise ValueError("Se necesitan como maximo 100 rondas para jugar")
        return rounds
