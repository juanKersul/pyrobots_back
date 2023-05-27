from fastapi import APIRouter
from fastapi import HTTPException
from controllers.security.tokens import generate_token
from controllers.security.password import decrypt_password
from models.db.database import database
from models.crud.user_services import check_user
from models.crud.user_services import search_user

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
            raise HTTPException(
                status_code=400, detail="Contraseña incorrecta"
                )
    else:
        raise HTTPException(status_code=400, detail="El usuario no existe")
