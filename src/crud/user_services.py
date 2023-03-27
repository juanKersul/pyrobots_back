from src.db.entities import User
from pony.orm import db_session, commit
import random
from pony.orm import ObjectNotFound, OperationalError


@db_session()
def add_user(new_username: str, new_password_encripted: str, new_email: str):
    """
    Agrega un usuario a la base de datos
    Args: new_username (str): Nombre de usuario
          new_password_encripted (str): Contraseña encriptada
          new_email (str): Email del usuario
    Returns:
        bool: True si se agrego correctamente, False si no
    """
    validation_code = "".join(random.sample(new_password_encripted[7:13], 6))
    with db_session:
        try:
            User(
                username=new_username,
                password=new_password_encripted,
                confirmation_mail=False,
                email=new_email,
                validation_code=validation_code,
                avatar="default.jpeg",
            )
            commit()
        except OperationalError("el nombre de usuario ya existe"):
            raise


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
        user = User[username]
        if not (code == user.validation_code and user.confirmation_mail):
            user.confirmation_mail = True
    except OperationalError("bad username or confirmation code"):
        raise


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
        return code
    except ObjectNotFound("no existe el usuario"):
        raise


@db_session()
def search_user(name: str):
    """Busca un usuario en la base de datos por su nombre.
    Args:
        name (Any): nombre del usuario a buscar.
    Returns:
        Any: ??
    """
    try:
        data = User.get(username=name)
        return data
    except ObjectNotFound("no existe el usuario"):
        raise


@db_session
def search_user_by_email(input_email: str):
    """Busca un usuario en la base de datos por su email.
    Args:
        input_email (Any): email del usuario a buscar.
    Returns:
        Any: ??
    """
    try:
        data = User.select(lambda p: p.email == input_email).get()
        return data
    except ObjectNotFound("no existe el usuario"):
        raise


@db_session
def store_user_avatar(username: str, file: str):
    """_summary_

    Args:
        username (str): nombre de usuario
        file (str): nombre del archivo
    """
    with db_session:
        try:
            new_filename = file.filename.split(".")
            new_filename[0] = username + "."
            file.filename = "".join(new_filename)
            User[username].avatar = file.filename
        except OperationalError("el usuario no existe"):
            raise
