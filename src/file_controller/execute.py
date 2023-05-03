from game.command import Command


def execute_file(path: str, filename: str):
    exec(open(path).read(), globals())
    object = globals()[filename]
    return object
