from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        # current
        self.position = (None, None)
        self.life = None
        self.scan_result = None
        # required
        self.cannon_target = (None, None)
        self.active_cannon = None

        self.scanner_target = (None, None)
        self.active_scanner = None

        self.direction = None
        self.velocity = None

    # abstract methods
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def respond(self):
        pass

    # getters

    def get_direction(self):
        return self.direction

    def get_position(self):
        return self.position

    def get_life(self):
        return self.life

    def scanned(self):
        """Devuelve el resultado del escaneo de la ronda previo. Devuelve la
        distancia al robot más cercano en la dirección apuntada.

        Returns:
            int: Distancia al robot más cercano.
        """
        return self.scan_result

    # setters
    def drive(self, degree, velocity):
        self.direction = degree
        self.velocity = velocity

    def cannon(self, degree, distance):
        """Cuando se llama a este método, se prepara el cañón para disparar.
        Si se llama a este método dos veces seguidas, sólo la última tiene
        efecto. Recién se ejecuta el disparo al finalizar la ronda.

        Args:
            degree (Any): Grados a lo que voy a disparar.
            distance (Any): Distancia a la que voy a disparar.
        """
        self.cannon_target = (degree, distance)
        self.active_cannon = True

    def point_scanner(self, direction, resolution_in_degrees):
        """Con este método se puede apuntar el escáner en cualquier dirección.
        Pero el resultado del escaneo estará disponible en la siguiente ronda,
        a través del siguiente método.

        Args:
            direction (Any): Dirección a la que se desea apuntar el scanner.
            resolution_in_degrees (Any): Amplitud del scanner.
        """
        self.scanner_target = (direction, resolution_in_degrees)
        self.active_scanner = True

    def get_state(self):
        return (
            self.cannon_target,
            self.active_cannon,
            self.scanner_target,
            self.active_scanner,
            self.velocity,
            self.direction,
        )

    def set_state(self, position, life, scan_result):
        self.position = position
        self.life = life
        self.scan_result = scan_result
        self.active_cannon = False
        self.active_scanner = False
