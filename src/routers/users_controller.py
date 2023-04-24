from fastapi import APIRouter
from fastapi import HTTPException
from crud.user_services import add_user
from crud.user_services import search_user
from crud.user_services import update_confirmation
from crud.user_services import check_user
from crud.user_services import check_email
from security.password import encrypt_password
from security.validation_code import generate_validation_code
from mail2.email_service import send_confirmation_mail
from db.database import database

user_end_points = APIRouter()


@user_end_points.post("/Users")
async def user_register(username: str, password: str, email: str):
    """Registrar usuario
    Args:
        user_to_add (User_base): usuario a registrar

    Raises:
        HTTPException: IntegrityError:409, el usuario ya existe.
        HTTPException: IntegrityError:409, el email ya existe.
        HTTPException: 400: el usuario no existe.
    Returns:
        dict[str, str]: {"Status": msg}
    """
    if check_user(database, username):
        raise HTTPException(
            status_code=409, detail="El nombre " + username + " ya esta en uso"
        )
    elif check_email(database, email):
        raise HTTPException(
            status_code=409, detail="El email " + email + " ya esta en uso"
        )
    else:
        encripted_password = encrypt_password(password)
        validation_code = generate_validation_code(6)
        add_user(database, username, encripted_password, email, validation_code)
        await send_confirmation_mail(email, username, validation_code)
        return {"Status": "Usuario creado con exito"}


@user_end_points.put("/Users/{username}/verify")
def user_verification(username: str, code: str):
    """Verificación de usuario

    Args:
        username (str): username
        code (str): token

    Raises:
        HTTPException: 400: el usuario no existe
        HTTPException: 400 el token no es válido

    Returns:
        dict[str, str]: {"Status": msg}
    """
    if check_user(database, username):
        user = search_user(database, username)
        if user.validation_code == code:
            update_confirmation(database, username, True)
            return {"Status": "Usuario verificado con exito"}
        else:
            raise HTTPException(status_code=400, detail="El codigo no es valido")
    else:
        raise HTTPException(status_code=400, detail="El usuario no existe")
