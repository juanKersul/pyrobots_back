from math import sqrt


def distance(t1: tuple, t2: tuple):
    res = round(sqrt((t2[0] - t1[0]) ** 2 + (t2[1] - t1[1]) ** 2))
    return res


# asdasd
def danio_misil(robot_position: tuple, misil_position: tuple):
    if misil_position == (None, None):
        danio = 0
    elif distance(robot_position, misil_position) <= 10:
        danio = 10
    elif distance(robot_position, misil_position) <= 30:
        danio = 5
    elif distance(robot_position, misil_position) <= 60:
        danio = 3
    else:
        danio = 0
    return danio


def danio_colision(pos_r1: tuple, pos_r2: tuple):
    danio = 0
    if distance(pos_r1, pos_r2) <= 20:
        danio = 2
    return danio


def danio_pared(pos_r: tuple):
    danio = 0
    if (pos_r[0] == 0) or (pos_r[0] == 999):
        danio = 2
    elif (pos_r[1] == 0) or (pos_r[1] == 999):
        danio = 2
    return danio


def inflingir_danio(robot, other_robots):
    """Inflinge daño a robots.

    Args:
        robot (Any): Robot actual
        other_robots (Any): Robots a los que dañar.
    """

    if robot.current_damage > 0:
        danio_p = danio_pared(robot.current_position)
        robot.current_damage -= danio_p

    for robot_check in other_robots:
        danio_c = danio_colision(robot.current_position, robot_check.current_position)
        if robot.current_damage > 0:
            robot.current_damage -= danio_c
        if robot_check.current_damage > 0:
            robot_check.current_damage -= danio_c

    for robot_x in other_robots:
        # Revisar daño por misil
        if robot.current_velocity < 80 and robot.current_damage > 0:
            danio2 = danio_misil(robot.current_position, robot_x.misil_position)
            robot.current_damage -= danio2

    if robot.current_damage < 0:
        robot.current_damage = 0


def avanzar_ronda(robots: list):
    """Avanza de ronda

    Args:
        robots (list): Lista de robots que participan de la ronda.

    Returns:
        List[]: Resultado de rondas
    """
    results_by_robots = []

    for robot in robots:
        other_robots = robots.copy()
        other_robots.remove(robot)

        inflingir_danio(robot, other_robots)

    # respond
    for robot in robots:
        if robot.current_damage > 0:
            try:
                robot.respond()
            except:
                pass
    # scan
    for robot in robots:
        if robot.current_damage > 0:
            other_robots = robots.copy()
            other_robots.remove(robot)
            fun = lambda x: True if x.current_damage > 0 else False
            other_robots = filter(fun, other_robots)
            scan_list = [r.current_position for r in other_robots]
            robot._scan(scan_list)
    # atack
    for robot in robots:
        if robot.current_damage > 0:
            robot._shoot()
        else:
            robot.misil_position = (None, None)
    # move
    for robot in robots:
        if robot.current_damage > 0:
            robot.last_position = robot.current_position
            robot._move()
    # generate json
    for robot in robots:
        if robot.current_damage > 0:
            result_round = {
                "id": None,  # Se carga afuera
                "x": robot.last_position[0],
                "y": robot.last_position[1],
                "xf": robot.current_position[0],
                "yf": robot.current_position[1],
                "nombre": None,  # Se carga afuera
                "vida": robot.current_damage,
                "mira": robot.current_direction,
                "motor": robot.current_velocity,
                "xmis": robot.last_position[0],
                "ymis": robot.last_position[1],
                "xmisf": robot.misil_position[0],
                "ymisf": robot.misil_position[1],
            }
            results_by_robots.append(result_round)
        else:
            result_round = {
                "id": None,  # Se carga afuera
                "x": robot.current_position[0],
                "y": robot.current_position[1],
                "xf": robot.current_position[0],
                "yf": robot.current_position[1],
                "nombre": None,  # Se carga afuera
                "vida": robot.current_damage,
                "mira": robot.current_direction,
                "motor": 0,
                "xmis": None,
                "ymis": None,
                "xmisf": None,
                "ymisf": None,
            }
            results_by_robots.append(result_round)

    return results_by_robots


def parse_robots(robot_list: list):
    """Dado un arreglo de id de robots devuelve el comportamiento
    correspondiente a ese id segun el archivo .py

    Args:
        robot_list (list): Lista de valores enteros que se corresponden con
        los id de los robots en la partida

    Returns:
        robots (list): Lista de objetos cuyas clases están definidas en
        un archivo .py.
    """
    robots = []
    for x in robot_list:
        file = get_file_by_id(x)
        if "default1" in file:
            file = "default1.py"
        elif "default2" in file:
            file = "default2.py"

        filename = "routers/robots/" + file
        exec(
            open(filename).read(),
            globals(),
        )
        file = file.strip(".py")
        file = file.split("_")[0]
        klass = globals()[file]
        r = klass((randint(100, 800), randint(100, 800)), randint(0, 360))
        robots.append(r)
    return robots


def add_robot_attributes(
    n_games: int, n_rounds: int, robots: list, robot_id_list: list
):
    """Dada una lista de objetos de robots, ejecuta n_games cantidad de juegos
    con n_rounds rondas cada una, y los devuelve en un arreglo de arreglos

    Args:
        n_games (int): Cantidad de juegos a jugar en la partida
        n_rounds (int): Cantidad de rondas que cada juego va a tener
        robots (list): Lista de objetos que contiene comportamiento de los robots
        robot_id_list (list): Lista de los id de cada robot en partida

    Returns:
        outer_response (list): Arreglo de arreglos de arrreglos de objetos JSON
    """
    outer_response = []
    for i in range(n_games):
        outer_response.append(game(robots, n_rounds))
        for j in outer_response:
            for i in j:
                k = 0
                for j in i:
                    j["id"] = robot_id_list[k]
                    j["nombre"] = sc.get_robot_name(robot_id_list[k])
                    j["imagen"] = sc.get_robot_avatar(robot_id_list[k])
                    k += 1
    return outer_response


def games_last_round(outer_response: list):
    """Dado un arreglo de arreglos de arreglos de objetos JSON que representan
    la ejecucion de una partida devuelve el ultimo arreglo de objetos JSON de cada
    partida que representan la última ronda de la misma

    Args:
        outer_response (list): Arreglo de arreglos de arreglos de objetos JSON

    Returns:
        juego (list): Diccionario de valores que contiene la ultima ronda de
        cada juego.
    """
    final_round = []
    juego = {}
    contador = 0
    # Para cada partida
    for i in outer_response:
        contador += 1
        # Para rondas de partida
        for j in i:
            final_round.append(j)
        juego["Juego: " + str(contador)] = final_round[-1]
    return juego


def get_winners(juego: list):
    """Dado un diccionario de valores que contiene la ultima ronda de cada
    juego devuelve aquellos robots que aun estén vivos en la última ronda

    Args:
        juego (list): Diccionario de valores que contiene la ultima ronda de
        cada juego

    Returns:
        resultado: Diccionario que contiene los robots vivos al final de la
        ejecucion de cada juego
    """
    robots_sobrevivientes = []
    resultado = {}
    contador2 = 0
    for i in juego:
        contador2 += 1
        for j in juego[i]:
            if j["vida"] > 0:
                robots_sobrevivientes.append(j)
        resultado["Ganador/es juego: " + str(contador2)] = robots_sobrevivientes
        robots_sobrevivientes = []
    return resultado


def return_results(resultado: list):
    resultado2 = {}
    for i in resultado:
        for j in resultado[i]:
            resultado2[j["nombre"]] = 0
    for i in resultado:
        for j in resultado[i]:
            resultado2[j["nombre"]] += 1
    temp_value = 0
    ganador = {}
    for i in resultado2:
        if resultado2[i] > temp_value:
            temp_value = resultado2[i]
            ganador["ganador"] = i
    ganador["resultado"] = resultado2
    return ganador


def game(robots: list, rounds):
    """Ejecuta un juego

    Args:
        robots (list): Lista de robots de la simulación
        rounds (int): Cantidad de rondas del juego

    Returns:
        List[Any]: Lista de Rondas, un juego.
    """
    results_by_robots = []
    for robot in robots:
        if robot != None:
            try:
                robot.initialize()
            except:
                pass
    for i in range(rounds):
        results_by_robots.append(avanzar_ronda(robots))
    return results_by_robots
