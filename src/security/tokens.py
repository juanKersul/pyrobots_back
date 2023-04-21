from decouple import config
from datetime import datetime, timedelta
import jwt

# se obtienen de env
JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")
JWT_EXPIRES = timedelta(1)


def get_payload(userID: str):
    """Encodea el token.

    Args:
        userID (str): id del usuario.

    Returns:
        Dict[str,str]: {"id_usuario":"fecha de expiración"}
    """
    payload = {"userID": userID, "expiry": str(datetime.now() + JWT_EXPIRES)}
    return payload


def sign_JWT(userID: str):
    payload = get_payload(userID)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


# esta funcion decodea el token
def decode_JWT(token: str):
    """Decodea el token

    Args:
        token (str): token

    Returns:
        Dict[str, Any]: {"userID": "", "expiry": 0}
    """
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token
    except:
        return {"userID": "", "expiry": 0}
