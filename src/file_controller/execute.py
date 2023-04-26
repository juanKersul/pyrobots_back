from game.robot_class import Robot


def execute_file(path: str, filename: str):
    exec(open(path).read(), globals())
    object = globals()[filename]
    return object


