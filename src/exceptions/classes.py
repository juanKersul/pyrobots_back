class OperationalError (Exception):
    """Excepcion que representa un error operacional"""
    def __init__(self, message: str, error: Exception):
        error = error
        self.message = message
    pass


class ObjectNotFound (Exception):
    """Excepcion que representa que un objeto no fue encontrado"""
    def __init__(self, message: str):
        self.message = message
    pass


class ValidationError (Exception):
    """Excepcion que representa un error de validacion"""
    def __init__(self, message: str):
        self.message = message
    pass
