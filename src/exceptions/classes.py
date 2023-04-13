class OperationalError (Exception):
    """Excepcion que representa un error operacional"""
    def __init__(self, message: str):
        self.message = message


class ObjectNotFound (Exception):
    """Excepcion que representa que un objeto no fue encontrado"""
    def __init__(self, message: str):
        self.message = message
