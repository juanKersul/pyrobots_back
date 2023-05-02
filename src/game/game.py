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
