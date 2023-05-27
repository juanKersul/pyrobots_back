from math import sqrt
from math import degrees
from math import atan2
from abc import ABC, abstractmethod
from controllers.game.math import distance, polar_to_rect, amplitude_to_depth
from controllers.game.command import Command
from random import randint


class GameRobot(ABC):
    def __init__(self):
        self.life: int
        self.position: tuple[int, int]
        self.name: str
        self.misil_position: tuple[int, int]

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
            "position": self.position,
            "misil_position": self.misil_position,
        }

    @abstractmethod
    def get_damage(self, positions: list[tuple], damage: int, radius):
        pass

    def get_position(self):
        return self.position

    def get_misil_position(self):
        return self.misil_position


class Py_Robot(GameRobot):
    def __init__(
        self,
        name: str = "Py_Robot",
        command: Command = None,
    ):
        self.command = command
        self.name = name
        self.life = 100

        self.position = (randint(0, 999), randint(0, 999))
        self.misil_position = (None, None)
        self.scan_result = 1500

        self.cannon_target = (None, None)
        self.active_cannon = False

        self.scanner_target = (None, None)
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
            self.command.set_state(
                self.position,
                self.life,
                self.scan_result,
            )
            self.command.respond()
            (
                self.cannon_target,
                self.active_cannon,
                self.scanner_target,
                self.active_scanner,
                self.velocity,
                self.direction,
            ) = self.command.get_state()
        except Exception:
            self.life = 0

    def shoot(self):
        self.misil_position = (None, None)
        if self.active_cannon:
            misil_cordinates = polar_to_rect(
                ang=self.cannon_target[0],
                distance=self.cannon_target[1],
                origin=self.position,
            )
            self.misil_position = misil_cordinates
            self.active_cannon = False

    def move(self):
        self.position = polar_to_rect(self.direction, self.velocity, self.position)
        # wall colision
        if (
            self.position[0] == 0
            or self.position[0] == 999
            or self.position[1] == 0
            or self.position[1] == 999
        ):
            self.life -= 5

    def scan(self, robots_position: list):
        if self.active_scanner:
            # centrar el origen a la de main_pos
            main_pos = self.position
            robots_centered = [
                (r[0] - main_pos[0], r[1] - main_pos[1]) for r in robots_position
            ]
            # calcular cordenadas polares
            robots_polar_cordinates = [
                (degrees(atan2(r[1], r[0])) % 360, sqrt(r[0] ** 2 + r[1] ** 2))
                for r in robots_centered
            ]
            # filtrar segun distancia y angulo correcto
            amplitude = self.scanner_target[0] * 5
            max_distance = amplitude_to_depth(self.scanner_target[1])
            robots_f = [1500]
            for robot in robots_polar_cordinates:
                angleDiff = (self.scanner_target[0] - robot[0] + 180 + 360) % 360 - 180
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
            if distance(position, self.position) <= radius:
                self.life -= damage
