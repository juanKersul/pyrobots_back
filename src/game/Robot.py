from math import sqrt
from math import degrees
from math import atan2
from math import pi
from math import sin
from math import cos
from abc import ABC, abstractmethod


class Game_Robot(ABC):
    def __init__(self):
        self.life
        self.position
        self.name
        self.direction

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
            "direction": self.direction,
        }


class Py_Robot(Game_Robot):
    def __init__(
        self,
        initial_position: tuple = (None, None, None),
        life: int = 100,
        name: str = "Py_Robot",
    ):
        self.name = name
        self.current_position = initial_position
        self.current_velocity = 0
        self.cannon_ammo = 1
        self.misil_position = (None, None)
        self.cannon_target = (None, None)
        self.scanner_target = (None, None)
        self.last_position = initial_position
        self.life = life

        self.required_position = (None, None, None)
        self.required_velocity = 0
        self.scan_result = None

    def _distance(t1: tuple, t2: tuple):
        res = round(sqrt((t2[0] - t1[0]) ** 2 + (t2[1] - t1[1]) ** 2))
        return res

    def _polar_to_rect(ang, distance, origin):
        radian = float(ang * pi / 180)
        x = round(origin[0] + distance * cos(radian))
        y = round(origin[1] + distance * sin(radian))
        if x <= 0:
            x = 0
        if x >= 999:
            x = 999
        if y <= 0:
            y = 0
        if y >= 999:
            y = 999
        return (x, y)

    def _amplitude_to_depth(degre):
        result = -7.5 * (degre * 9) + 867
        return round(result)

    def shoot(self):
        misil_target = (None, None)
        if self.cannon_ammo <= 1:
            self.cannon_ammo = 0
            misil_target = self._polar_to_rect(
                ang=self.cannon_degree,
                distance=self.cannon_distance,
                origin=self.current_position,
            )
            self.misil_position = misil_target
            self.cannon_shoot = False
        else:
            self.cannon_ammo = 1
        self.misil_position = misil_target

    def move(self):
        # seting direction
        self.current_direction = self.required_direction
        # seting velocity
        self.current_velocity = self.required_velocity
        # seting position
        self.current_position = self._polar_to_rect(
            self.required_direction, self.required_velocity, self.current_position
        )
        # wall colision
        if (
            self.current_position[0] == 0
            or self.current_position[0] == 999
            or self.current_position[1] == 0
            or self.current_position[1] == 999
        ):
            self.life -= 5

    def scan(self, robots_position: list):
        # centrar el origen a la de main_pos
        main_pos = self.current_position
        robots_c = [(r[0] - main_pos[0], r[1] - main_pos[1]) for r in robots_position]
        # calcular cordenadas polares
        robots_p = [
            (degrees(atan2(r[1], r[0])) % 360, sqrt(r[0] ** 2 + r[1] ** 2))
            for r in robots_c
        ]
        # filtrar segun distancia y angulo correcto
        amplitude = self.resolution_in_degrees * 5
        max_distance = self._amplitude_to_depth(self.resolution_in_degrees)
        robots_f = [1500]
        for robot in robots_p:
            angleDiff = (self.direction_scanner - robot[0] + 180 + 360) % 360 - 180
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
            if self._distance(position, self.current_position) <= radius:
                self.life -= damage
