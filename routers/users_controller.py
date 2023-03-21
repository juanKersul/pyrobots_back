from fastapi import APIRouter, HTTPException,UploadFile
from starlette.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from decouple import config
from crud.user_services import (
    add_user,
    update_confirmation,
    get_code_for_user,
    search_user_by_email,
    search_user,
    sign_JWT,
    decrypt_password,
    store_user_avatar,
    decode_JWT,
    get_user_from_db
)
from schemas.iuser import User_base, User_login_schema
from crud.robot_service import add_default_robot
import shutil
from datetime import datetime
import base64
user_end_points = APIRouter()


@user_end_points.post("/login")
async def user_login(credentials: User_login_schema):
    """Iniciar Sesión.

    Args:
        credentials (User_login_schema): credenciales, username o email, y contraseña.

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
            raise HTTPException(
                status_code=400,
                detail="email no verificado"
                )
        else:
            response = sign_JWT(credentials.username)
            return {"token": response}


@user_end_points.post("/register")
async def user_register(user_to_add: User_base):
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
    msg = add_user(new_user=user_to_add)
    if ('IntegrityError' in msg and 'username' in msg):
        raise HTTPException(
            status_code=409,
            detail="El nombre de usuario ya existe"
            )
    if ('IntegrityError' in msg and 'email' in msg):
        raise HTTPException(
            status_code=409,
            detail="El email ya existe"
            )
    code_validation = get_code_for_user(user_to_add.username)
    if "no existe" in code_validation:
        raise HTTPException(
            status_code=400,
            detail="El usuario "+user_to_add.username+" no existe"
            )
    await send_confirmation_mail(
        user_to_add.email,
        code_validation,
        user_to_add.username
        )
    return {"Status": msg}


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
            status_code=400,
            detail="El usuario "+username+" no existe"
            )
    if msg == "El codigo de confirmacion no es valido":
        raise HTTPException(
            status_code=400,
            detail=msg
            )
    if (msg == "Usuario confirmado con exito"):       
        add_default_robot(username)
    response = RedirectResponse(url='http://localhost:3000/home/login')
    return response


MAIL_USERNAME_S = config("MAIL_USERNAME")
MAIL_PASSWORD_S = config("MAIL_PASSWORD")
MAIL_PORT_S = config("MAIL_PORT")
MAIL_SERVER_S = config("MAIL_SERVER")


async def send_confirmation_mail(
        email: str,
        code_validation: str,
        username: str
        ):
    """Envía mail de confirmación.

    Args:
        email (str): email al que enviar la confirmación.
        code_validation (str): código a enviar.
        username (str): usuario al que enviar.
    """
    conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME_S,
        MAIL_PASSWORD=MAIL_PASSWORD_S,
        MAIL_FROM=email,
        MAIL_PORT=MAIL_PORT_S,
        MAIL_SERVER=MAIL_SERVER_S,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
    )
    html = open("email.html", "r")
    template = html.read().format(
        user=username,
        end_point_verify=code_validation
        )
    message = MessageSchema(
        subject="Mail de confirmación pyRobots",
        recipients=[email],
        body=template,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)

@user_end_points.post("/ReplaceUserImage")
async def replace_user_image(token:str,file:UploadFile):
    res =store_user_avatar(token,file)
    if res != "token invalido": 
        store_Userimg(file)
        return {"imagen guardada con exito"}
    else:
        raise HTTPException(status_code=400,detail="token invalido")

def store_Userimg(file: UploadFile):
    file.file.seek(0)
    with open("routers/users/avatars/" + file.filename, "wb+") as upload_folder:
        shutil.copyfileobj(file.file, upload_folder)

@user_end_points.get("/GetUser")
def get_user(token):
    user = get_user_from_db(token)
    if (user != "token invalido"):
        path = "routers/users/avatars/"+str(user.avatar)
        with open(path, 'rb') as f:
            base64image = base64.b64encode(f.read())
        return {"username":user.username,"email":user.email,"avatar":base64image}
    else:
        raise HTTPException(status_code=400,detail="token invalido")