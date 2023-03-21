from math import sqrt
from routers.robot.robot_class import Robot
def distance(t1: tuple, t2: tuple):
    res = round(sqrt((t2[0]-t1[0])**2 + (t2[1]-t1[1])**2))
    return res 
#asdasd
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


def inflingir_danio(robot,other_robots):
    """Inflinge daño a robots.

    Args:
        robot (Any): Robot actual
        other_robots (Any): Robots a los que dañar.
    """

    if(robot.current_damage>0):
        danio_p = danio_pared(robot.current_position)
        robot.current_damage -= danio_p
    
    for robot_check in other_robots:
        danio_c = danio_colision(
            robot.current_position, robot_check.current_position
        )
        if (robot.current_damage>0):
            robot.current_damage -= danio_c
        if (robot_check.current_damage>0):    
            robot_check.current_damage -= danio_c
    
    for robot_x in other_robots:
        # Revisar daño por misil
        if (robot.current_velocity < 80 and robot.current_damage>0):
            danio2 = danio_misil(robot.current_position, robot_x.misil_position)
            robot.current_damage -= danio2
    
    if(robot.current_damage<0):
        robot.current_damage = 0
        
def avanzar_ronda(robots:list):
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
        
        inflingir_danio(robot,other_robots)
    
    #respond
    for robot in robots:
        if robot.current_damage > 0:
            try:
                robot.respond()
            except:
                pass
    #scan
    for robot in robots:
       if robot.current_damage > 0:
           other_robots = robots.copy()
           other_robots.remove(robot)
           fun = lambda x : True if x.current_damage >0 else False
           other_robots = filter(fun,other_robots)
           scan_list = [r.current_position for r in other_robots]
           robot._scan(scan_list)
    #atack
    for robot in robots:
        if robot.current_damage > 0:
            robot._shoot()
        else:
            robot.misil_position = (None,None)
    #move
    for robot in robots:
        if robot.current_damage > 0:
            robot.last_position = robot.current_position
            robot._move()
    #generate json
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
