from controllers.game.command import Command
from exceptions.classes import ObjectNotFound


def execute_file(path: str, filename: str):
    try:
        exec(open(path).read(), globals())
    except Exception:
        raise ObjectNotFound("Robot file not found")
    try:
        clase = globals()[filename]
    except Exception:
        raise ObjectNotFound("Robot class not found")
    object = clase()
    return object
