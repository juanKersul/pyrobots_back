from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        # current
        self.position_x
        self.position_y
        self.life
        self.scan_result
        # required
        self.cannon_target_ang
        self.cannon_target_dis
        self.active_cannon

        self.scanner_target_ang
        self.scanner_target_amp
        self.active_scanner

        self.direction
        self.velocity

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

    def get_damage(self):
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
        self.cannon_target_ang = degree
        self.cannon_target_dis = distance
        self.active_cannon = True

    def point_scanner(self, direction, resolution_in_degrees):
        """Con este método se puede apuntar el escáner en cualquier dirección.
        Pero el resultado del escaneo estará disponible en la siguiente ronda,
        a través del siguiente método.

        Args:
            direction (Any): Dirección a la que se desea apuntar el scanner.
            resolution_in_degrees (Any): Amplitud del scanner.
        """
        self.scanner_target_ang = direction
        self.scanner_target_amp = resolution_in_degrees
        self.active_scanner = True

    def get_atributes(self):
        return (
            self.cannon_target_ang,
            self.cannon_target_dis,
            self.active_cannon,
            self.scanner_target_ang,
            self.scanner_target_amp,
            self.active_scanner,
        )

    def set_atributes(self, position_x, position_y, life, scan_result):
        self.position_x = position_x
        self.position_y = position_y
        self.life = life
        self.scan_result = scan_result
