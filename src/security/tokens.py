from decouple import config
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from exceptions.classes import OperationalError
from jwt import decode
from jwt import encode
from jwt import PyJWTError
from jwt import ExpiredSignatureError
from jwt import InvalidSignatureError
from fastapi import HTTPException

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
def authorize_token(token: str):
    try:
        decode_token = decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token["userID"]
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="sesion expirada")
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="token invalido")
    except PyJWTError as e:
        raise OperationalError("No se pudo decodificar el token", e)
