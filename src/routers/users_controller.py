from fastapi import APIRouter
from fastapi import HTTPException
from starlette.responses import RedirectResponse
from crud.user_services import add_user
from crud.user_services import search_user
from crud.user_services import update_confirmation
from crud.user_services import check_user
from crud.user_services import check_email
from schemas.iuser import User_login_schema
from security.password import encrypt_password
from security.validation_code import generate_validation_code
from mail2.email_service import send_confirmation_mail
from db.database import database

user_end_points = APIRouter()


@user_end_points.post("/login")
async def user_login(credentials: User_login_schema):
    """Iniciar Sesión.
    Args:
        credentials (User_login_schema): credenciales, username o email,
        y contraseña.

    Raises:
        HTTPException: 400: el usuario no existe.
        HTTPException: 400: contraseña incorrecta.
        HTTPException: 400: email no verificado.

    Returns:
        dict[str:str]: {"token": response}
    """
    if credentials.username == "":
        data = search_user_by_email(credentials.email)
    else:
        data = search_user(credentials.username)

    if data is None:
        raise HTTPException(status_code=400, detail="no existe el usuario")
    else:
        pass_decrypt = decrypt_password(data.password)
        mail_is_verificated = data.confirmation_mail
        password_is_correct = credentials.password == pass_decrypt

        if not password_is_correct:
            raise HTTPException(status_code=400, detail="contrasenia incorrecta")
        elif not mail_is_verificated:
            raise HTTPException(status_code=400, detail="email no verificado")
        else:
            response = sign_JWT(credentials.username)
            return {"token": response}


@user_end_points.post("/register")
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


@user_end_points.get("/verify")
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
    msg = update_confirmation(username, code)
    if "no existe" in msg:
        raise HTTPException(
            status_code=400, detail="El usuario " + username + " no existe"
        )
    if msg == "El codigo de confirmacion no es valido":
        raise HTTPException(status_code=400, detail=msg)
    if msg == "Usuario confirmado con exito":
        add_default_robot(username)
    response = RedirectResponse(url="http://localhost:3000/home/login")
    return response
