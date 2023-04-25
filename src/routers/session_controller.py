from fastapi import APIRouter
from fastapi import HTTPException
from security.tokens import generate_token
from security.password import decrypt_password
from db.database import database
from crud.user_services import check_user
from crud.user_services import search_user
from security.tokens import decode_token

session_end_points = APIRouter()


@session_end_points.post("/session")
async def user_login(username: str, password: str):
    if check_user(database, username):
        user = search_user(database, username)
        if decrypt_password(user.password) == password:
            if user.confirmation_mail:
                token = generate_token(username)
                return {"Status": "Usuario logueado con exito", "token": token}
            else:
                raise HTTPException(
                    status_code=400, detail="El usuario no esta confirmado"
                )
        else:
            raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    else:
        raise HTTPException(status_code=400, detail="El usuario no existe")


async def authorization(token: str):
    if token is None:
        raise HTTPException(status_code=401, detail="No autorizado")
    else:
        active, payload = decode_token(token)
        if active:
            return payload["username"]
        else:
            raise HTTPException(status_code=401, detail="No autorizado")
