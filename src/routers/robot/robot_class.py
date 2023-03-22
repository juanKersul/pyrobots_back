from math import sin, cos, pi, sqrt, degrees, atan2
from decouple import config

ACELERATION_FACTOR = int(config("aceleration"))
MAX_VELOCITY = int(config("maxvelocity"))
SPIN_FACTOR = int(config("spinFactor"))


class Robot:
    """Crea un robot.
    """
    def __init__(
        self,
        position: tuple = None,
        direction: int = None,
    ):
        self.current_position = position
        self.last_position = position
        self.current_damage = 100
        self.current_direction = direction
        self.current_velocity = 0
        self.cannon_ammo = 1
        self.required_direction = 0
        self.required_velocity = 0
        self.cannon_degree = 0
        self.cannon_distance = 0
        self.cannon_shoot = False
        self.misil_position = (None, None)
        self.direction_scanner = 0
        self.resolution_in_degrees = 10
        self.scanner_range = 100
        self.scan_result = 1500

    # Cañón
    def is_cannon_ready(self):
        """Cuando se dispara un misil, el cañón requiere un tiempo
        para recargarse. Se puede usar esta función para chequear si
        el cañón está completamente recargado"""
        return self.cannon_ammo == 1

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

    # status
    def get_position(self):
        return self.current_position

    def get_velocity(self):
        return self.current_velocity

    def get_damage(self):
        return self.current_damage
    def get_direction(self):
        return self.current_direction

    def _shoot(self):
        misil_target = (None, None)
        if self.is_cannon_ready() and self.cannon_shoot:
            self.cannon_ammo = 0
            misil_target = polar_to_rect(
                ang=self.cannon_degree,
                distance=self.cannon_distance,
                origin=self.current_position,
            )
            self.misil_position = misil_target
            self.cannon_shoot = False
        else:
            self.cannon_ammo = 1
        self.misil_position = misil_target
    
    def _move(self):
        # seting direction
        self.current_direction = block_direction(self.current_direction, self.current_velocity, self.required_direction)
        # seting velocity
        self.current_velocity = calc_velocity(self.required_velocity, self.current_velocity)
        # seting position
        self.current_position = polar_to_rect(self.required_direction, self.required_velocity, self.current_position)

    # Escáner
    # Setter
    def point_scanner(self, direction, resolution_in_degrees):
        """Con este método se puede apuntar el escáner en cualquier dirección.
        Pero el resultado del escaneo estará disponible en la siguiente ronda,
        a través del siguiente método.

        Args:
            direction (Any): Dirección a la que se desea apuntar el scanner.
            resolution_in_degrees (Any): Amplitud del scanner.
        """
        # Set scan direction
        if direction < 0:
            direction = -direction
        elif direction >= 360:
            direction %= 360

        self.direction_scanner = direction
        self.resolution_in_degrees = resolution_in_degrees

    # Getter
    def scanned(self):
        """Devuelve el resultado del escaneo de la ronda previo. Devuelve la
        distancia al robot más cercano en la dirección apuntada.

        Returns:
            int: Distancia al robot más cercano.
        """
        return self.scan_result

    # Setter
    def _scan(self, robots_position: list):
        # centrar el origen a la de main_pos
        main_pos = self.current_position
        robots_c = [(r[0]-main_pos[0],r[1]-main_pos[1]) for r in robots_position]
        # calcular cordenadas polares 
        robots_p = [(degrees(atan2(r[1],r[0])) % 360 , sqrt(r[0]**2+r[1]**2)) for r in robots_c]
        #filtrar segun distancia y angulo correcto
        amplitude = self.resolution_in_degrees*5
        max_distance = amplitude_to_depth(self.resolution_in_degrees)
        robots_f = [1500]
        for robot in robots_p:
            angleDiff = (self.direction_scanner - robot[0] + 180 + 360) % 360 - 180
            if(angleDiff>=-amplitude and angleDiff <= amplitude and robot[1]<max_distance):
                robots_f.append(robot[1])
        #calcular el minimo
        res = min(robots_f)
        self.scan_result = res
         

def amplitude_to_depth(degre):
    """Toma una apertura de 1 a 10 y
    retorna la profundidad en metros que se van a escanear.
    degre = 1 --> 1000m
    ...
    degre = 10 --> 100m

    Args:
        degre (Any): amplitud del scanner.

    Returns:
        Any: profundidad del scanner.
    """
    result = -7.5 * (degre*9) + 867 
    return round(result)

def calc_velocity(required_velocity, current_velocity):
    # sanitize input
    if required_velocity > 100:
        new_velocity = 100
    elif required_velocity < 0:
        new_velocity = 0
    else:
        new_velocity = required_velocity
    # calc velocity
    if (new_velocity < current_velocity):
        decrease = (MAX_VELOCITY - new_velocity) * ACELERATION_FACTOR / MAX_VELOCITY
        if decrease < 0:
            decrease = 0
        if current_velocity - decrease < 0:
            return 0
        else:
            return current_velocity - decrease
    elif (new_velocity>current_velocity):
        increase = new_velocity * ACELERATION_FACTOR / MAX_VELOCITY
        if increase > MAX_VELOCITY:
            increase = MAX_VELOCITY
        return current_velocity + increase
    else:
        return current_velocity


def block_direction(current_direction, current_velocity, required_direction):
    new_direction = required_direction % 360
    if new_direction < 0:
        new_direction = new_direction + 360
    if current_velocity <= 50:
        return new_direction
    else:
        right_limit = (current_direction - SPIN_FACTOR) % 360
        left_limit = (current_direction + SPIN_FACTOR) % 360
        if new_direction < right_limit:
            return right_limit
        elif new_direction > left_limit:
            return left_limit
        else:
            return new_direction

def polar_to_rect(ang, distance, origin):
        
    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]
        div = det(xdiff, ydiff)
        if div == 0:
            return (0,0)
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return int(x), int(y)
    cuad = -1
    radian = float(ang * pi /180) 
    x = round(origin[0] + distance * cos(radian))
    y = round(origin[1] + distance * sin(radian))
    A = (0,0)
    B = (0,0)
    C = (0,0)
    D = (0,0)
    if(x>=0 and x<1000 and y>=0 and y<1000):
        res = (x,y)
    else:
        A = (origin[0],origin[1])
        B = (x,y)
        # Cuadrante izquierdo
        if(x<0):
            cuad = 0
            C = (0,0)
            D = (0,999)
            # Cuadrante inferior
            if(y<0):
                C = (0,0)
                D = (999,0)
            # Cuadrante superior
            elif(y>999):
                C = (0,999)
                D = (999,999)
        # Cuadrante derecho
        elif(x>999):
            cuad = 2
            C = (999,0)
            D = (999,999) 
            # Cuadrante inferior
            if(y<0):
                C = (0,0)
                D = (999,0)
            # Cuadrante superior
            elif(y>999):
                C = (0,999)
                D = (999,999)
        # Cuadrante inferior
        elif(y<0):
            cuad = 3
            C = (0,0)
            D = (999,0)
            # Cuadrante izquierdo
            if (x<0):
                C = (0,0)
                D = (0,999)
            # Cuadrante derecho
            elif (x>999):
                C = (999,0)
                D = (999,999)
        # Cuadrante superior
        elif(y>999):
            cuad = 1
            C = (0,999)
            D = (999,999)
            if (x<0):
                C = (0,0)
                D = (0,999)
            # Cuadrante derecho
            elif(x>999):
                C = (999,0)
                D = (999,999)
        res = line_intersection((A, B), (C, D))
        if(res[0]<0 or res[0]>999 or res[1]<0 or res[1]>999):
            if cuad == 0:
                C = (0,0)
                D = (0,999)
            elif cuad == 1:
                C = (0,999)
                D = (999,999)
            elif cuad == 2:
                C = (999,0)
                D = (999,999)
            elif cuad == 3:
                C = (0,0)
                D = (999,0)
            res = line_intersection((A, B), (C, D))
    return (res[0],res[1])