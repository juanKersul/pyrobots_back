from pydantic import BaseModel


class RobotBase(BaseModel):
    name: str
    avatar: str
    matchs_pleyed: int
    matchs_won: int
    avg_life_time: float


class Robot(RobotBase):
    id: int

    class Config:
        orm_mode = True
