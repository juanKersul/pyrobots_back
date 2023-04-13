from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import UploadFile
from starlette.responses import RedirectResponse
import crud.user_services as user_service
from schemas.iuser import User_base
from schemas.iuser import User_login_schema
import shutil
import base64

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
    user_service.add_user(new_user=user_to_add)
    

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


@user_end_points.post("/ReplaceUserImage")
async def replace_user_image(token: str, file: UploadFile):
    res = store_user_avatar(token, file)
    if res != "token invalido":
        store_Userimg(file)
        return {"imagen guardada con exito"}
    else:
        raise HTTPException(status_code=400, detail="token invalido")


def store_Userimg(file: UploadFile):
    file.file.seek(0)
    with open("routers/users/avatars/" + file.filename, "wb+") as upload_folder:
        shutil.copyfileobj(file.file, upload_folder)


@user_end_points.get("/GetUser")
def get_user(token):
    user = get_user_from_db(token)
    if user != "token invalido":
        path = "routers/users/avatars/" + str(user.avatar)
        with open(path, "rb") as f:
            base64image = base64.b64encode(f.read())
        return {"username": user.username, "email": user.email, "avatar": base64image}
    else:
        raise HTTPException(status_code=400, detail="token invalido")
