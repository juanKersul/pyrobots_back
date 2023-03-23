from db.entities import User
from pony.orm import db_session, commit
import random


@db_session()
def add_user(
    new_username,
    new_password_encripted,
    new_email,
):
    """Agrega un usuario a la base de datos, devolviendo un
    mensaje representativo del estado de la salida
    Args:
        new_user (User_create): Usuario a persistir
    Returns:
        str: representativa del estado de la salida
    """
    code_for_validation = "".join(random.sample(new_password_encripted[7:13], 6))
    with db_session:
        try:
            User(
                username=new_username,
                password=new_password_encripted,
                confirmation_mail=False,
                email=new_email,
                validation_code=code_for_validation,
                avatar="default.jpeg",
            )
            commit()
        except Exception as e:
            return str(e)
        return "Usuario agregado con exito"


@db_session
def update_confirmation(username: str, code: str):
    """Actualiza el valor del atributo que representa que
    el la cuenta fue confirmada
    Args:
        username (str): Usuario confirmado
        code (str): Codigo de privacidad para la validacion
    Returns:
        str: String representativa del estado de la salida
    """
    try:
        user_for_validate = User[username]
    except Exception as e:
        return str(e) + " no existe"
    if (
        code == user_for_validate.validation_code
        and user_for_validate.confirmation_mail == False
    ):
        user_for_validate.confirmation_mail = True
        return "Usuario confirmado con exito"
    elif (
        code == user_for_validate.validation_code
        and user_for_validate.confirmation_mail == True
    ):
        return "Intento volver a confirmar"
    return "El codigo de confirmacion no es valido"


@db_session
def get_code_for_user(username: str):
    """Trae el codigo de privacidad de la validacion
    de la base de datos
    Args:
        username (str): Usuario del cual queremos el codigo
    Returns:
        str: Codigo de privacidad
        Any: Error
    """
    try:
        code = User[username].validation_code
    except Exception as e:
        return str(e) + " no existe"
    return code


@db_session()
def search_user(name):
    """Busca un usuario en la base de datos por su nombre.
    Args:
        name (Any): nombre del usuario a buscar.
    Returns:
        Any: ??
    """
    data = User.get(username=name)
    return data


@db_session
def search_user_by_email(input_email):
    """Busca un usuario en la base de datos por su email.
    Args:
        input_email (Any): email del usuario a buscar.
    Returns:
        Any: ??
    """
    data = User.select(lambda p: p.email == input_email).get()
    return data


@db_session
def store_user_avatar(username, file):
    with db_session:
        try:
            new_filename = file.filename.split(".")
            new_filename[0] = username + "."
            file.filename = "".join(new_filename)
            User[username].avatar = file.filename
            return "todo bien"
        except:
            return "username invalido"


@db_session
def get_user_from_db(username):
    with db_session:
        try:
            res = User[username]
            return res
        except:
            return "username invalido"
