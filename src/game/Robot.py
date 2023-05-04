from math import sqrt
from math import degrees
from math import atan2
from abc import ABC, abstractmethod
from game.math import distance, polar_to_rect, amplitude_to_depth
from game.command import Command
from random import randint


class GameRobot(ABC):
    def __init__(self):
        self.life: int
        self.position_X: int
        self.position_Y: int
        self.name: str
        self.misil_position_X: int
        self.misil_position_Y: int

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def respond(self):
        pass

    @abstractmethod
    def scan(self, scan_list: list):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def shoot(self):
        pass

    def get_atributes(self):
        return {
            "name": self.name,
            "life": self.life,
            "positionX": self.position_X,
            "positionY": self.position_Y,
            "misil_position_X": self.misil_position_X,
            "misil_position_Y": self.misil_position_Y,
        }

    @abstractmethod
    def get_damage(self, positions: list[tuple], damage: int, radius):
        pass

    def get_position(self):
        return (self.position_X, self.position_Y)

    def get_misil_position(self):
        return (self.misil_position_X, self.misil_position_Y)


class Py_Robot(GameRobot):
    def __init__(
        self,
        initial_position: tuple = (randint(0, 999), randint(0, 999)),
        life: int = 100,
        name: str = "Py_Robot",
        command: Command = None,
    ):
        self.command = command
        self.name = name
        self.life = life

        self.position_X = initial_position[0]
        self.position_Y = initial_position[1]
        self.misil_position_X = None
        self.misil_position_Y = None
        self.scan_result = 1500

        self.cannon_target_ang = None
        self.cannon_target_dis = None
        self.active_cannon = False

        self.scanner_target_ang = None
        self.scanner_target_amp = None
        self.active_scanner = False

        self.direction = 0
        self.velocity = 0

    def initialize(self):
        try:
            self.command.initialize()
        except Exception:
            self.life = 0

    def respond(self):
        try:
            self.command.set_atributes(
                self.position_X,
                self.position_Y,
                self.life,
                self.scan_result,
            )
            self.command.respond()
            (
                self.cannon_target_ang,
                self.cannon_target_dis,
                self.active_cannon,
                self.scanner_target_ang,
                self.scanner_target_amp,
                self.active_scanner,
            ) = self.command.get_atributes()
        except Exception:
            self.life = 0

    def shoot(self):
        self.misil_position_X = None
        self.misil_position_Y = None
        if self.active_cannon:
            misil_cordinates = polar_to_rect(
                ang=self.cannon_target_ang,
                distance=self.cannon_target_dis,
                origin=(self.position_X, self.position_Y),
            )
            self.misil_position_X = misil_cordinates[0]
            self.misil_position_Y = misil_cordinates[1]
            self.active_cannon = False

    def move(self):
        self.position_X, self.position_Y = polar_to_rect(
            self.direction, self.velocity, (self.position_X, self.position_Y)
        )
        # wall colision
        if (
            self.position_X == 0
            or self.position_X == 999
            or self.position_Y == 0
            or self.position_Y == 999
        ):
            self.life -= 5

    def scan(self, robots_position: list):
        if self.active_scanner:
            # centrar el origen a la de main_pos
            main_pos = (self.position_X, self.position_Y)
            robots_centered = [
                (r[0] - main_pos[0], r[1] - main_pos[1]) for r in robots_position
            ]
            # calcular cordenadas polares
            robots_polar_cordinates = [
                (degrees(atan2(r[1], r[0])) % 360, sqrt(r[0] ** 2 + r[1] ** 2))
                for r in robots_centered
            ]
            # filtrar segun distancia y angulo correcto
            amplitude = self.scanner_target_ang * 5
            max_distance = amplitude_to_depth(self.scanner_target_amp)
            robots_f = [1500]
            for robot in robots_polar_cordinates:
                angleDiff = (self.scanner_target_ang - robot[0] + 180 + 360) % 360 - 180
                if (
                    angleDiff >= -amplitude
                    and angleDiff <= amplitude
                    and robot[1] < max_distance
                ):
                    robots_f.append(robot[1])
            # calcular el minimo
            res = min(robots_f)
            self.scan_result = res

    def get_damage(self, positions: list[tuple], damage: int, radius):
        for position in positions:
            if distance(position, (self.position_X, self.position_Y)) <= radius:
                self.life -= damage
