import string
import random


def generate_validation_code(longitude: int):
    """Genera un codigo de validacion para el usuario
    Returns:
        str: codigo de validacion
    """
    characters = string.ascii_letters + string.digits
    chain = ""
    for _ in range(longitude):
        chain += random.SystemRandom().choice(characters)
    return chain
