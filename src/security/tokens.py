from decouple import config
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from exceptions.classes import OperationalError
from jwt import decode
from jwt import encode
from jwt import PyJWTError
from jwt import ExpiredSignatureError

# se obtienen de env
JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")
JWT_EXPIRES = timedelta(minutes=int(config("JWT_EXPIRES")))


def generate_token(userID: str):
    payload = {"userID": userID, "exp": datetime.now(tz=timezone.utc) + JWT_EXPIRES}
    try:
        token = encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    except PyJWTError as e:
        raise OperationalError("No se pudo generar el token", e)


# esta funcion decodea el token
def decode_token(token: str):
    """Decodea el token

    Args:
        token (str): token

    Returns:
        Dict[str, Any]: {"userID": "", "expiry": 0}
    """
    try:
        decode_token = decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return True, decode_token
    except ExpiredSignatureError:
        return False, {}
    except PyJWTError as e:
        raise OperationalError("No se pudo decodificar el token", e)
