from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        # current
        self.current_position = (None, None)
        self.current_direction = 0
        self.currrent_velocity = 0
        self.cannon_ammo = 1
        self.life = 100
        self.scan_result = 1500
        # required
        self.required_position = (None, None)
        self.required_direction = 0
        self.required_velocity = 0
        self.cannon_degree = 0
        self.cannon_distance = 0
        self.scanner_direction = 0

    # abstract methods
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def respond(self):
        pass

    # getters

    def get_position(self):
        return self.current_position

    def get_velocity(self):
        return self.currrent_velocity

    def get_damage(self):
        return self.life

    def get_direction(self):
        return self.current_direction

    def is_cannon_ready(self):
        """Cuando se dispara un misil, el cañón requiere un tiempo
        para recargarse. Se puede usar esta función para chequear si
        el cañón está completamente recargado"""
        return self.cannon_ammo == 1

    def scanned(self):
        """Devuelve el resultado del escaneo de la ronda previo. Devuelve la
        distancia al robot más cercano en la dirección apuntada.

        Returns:
            int: Distancia al robot más cercano.
        """
        return self.scan_result

    # setters
    def drive(self, degree, velocity):
        self.required_direction = degree
        self.required_velocity = velocity

    def cannon(self, degree, distance):
        """Cuando se llama a este método, se prepara el cañón para disparar.
        Si se llama a este método dos veces seguidas, sólo la última tiene
        efecto. Recién se ejecuta el disparo al finalizar la ronda.

        Args:
            degree (Any): Grados a lo que voy a disparar.
            distance (Any): Distancia a la que voy a disparar.
        """
        if distance > 700:
            distance = 700
        if distance < 0:
            distance = 0
        if degree > 360:
            degree = 360
        if degree < 0:
            degree = 0
        self.cannon_shoot = True
        self.cannon_degree = degree
        self.cannon_distance = distance

    def point_scanner(self, direction, resolution_in_degrees):
        """Con este método se puede apuntar el escáner en cualquier dirección.
        Pero el resultado del escaneo estará disponible en la siguiente ronda,
        a través del siguiente método.

        Args:
            direction (Any): Dirección a la que se desea apuntar el scanner.
            resolution_in_degrees (Any): Amplitud del scanner.
        """
        if direction < 0:
            direction = -direction
        elif direction >= 360:
            direction %= 360

        self.direction_scanner = direction
        self.resolution_in_degrees = resolution_in_degrees
