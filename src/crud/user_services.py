from pony.orm import db_session
from pony.orm import commit
from exceptions.classes import OperationalError
from pony.orm import OrmError
from pony.orm import exists


@db_session()
def add_user(
    db,
    new_username: str,
    new_password_encripted: str,
    new_email: str,
    validation_code: str,
):
    """
    Agrega un usuario a la base de datos
    Args:
        new_username (str): Nombre de usuario
        new_password_encripted (str): Contraseña encriptada
        new_email (str): Email del usuario
        validation_code (str): Codigo de validacion
    raises: OperationalError: Si no se puede agregar el usuario
    """
    try:
        db.User(
            username=new_username,
            password=new_password_encripted,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
    except OrmError as e:
        raise OperationalError("No se pudo agregar el usuario", e)
    commit()


@db_session
def update_confirmation(db, username: str, value: bool):
    """Actualiza el valor del atributo que representa que
    el la cuenta fue confirmada
    Args:
        username (str): nombre de usuario
        validation_code (str): Codigo de validacion
    Raises:
        ObjectNotFound: Si no se encuentra al usuario en la base de datos.
        OperationalError: Si no se puede actualizar el usuario
        OperationalError: Si no se puede obtener el usuario
    """
    try:
        user = db.User[username]
        user.confirmation_mail = value
    except OrmError as e:
        raise OperationalError("No se pudo actualizar el usuario", e)


@db_session
def update_validation_code(db, username: str, validation_code: str):
    """Actualiza el valor del atributo que representa que
    el la cuenta fue confirmada
    Args:
        username (str): nombre de usuario
        validation_code (str): Codigo de validacion
    Raises:
        ObjectNotFound: Si no se encuentra al usuario en la base de datos.
        OperationalError: Si no se puede actualizar el usuario
        OperationalError: Si no se puede obtener el usuario
    """
    try:
        user = db.User[username]
        user.validation_code = validation_code
    except OrmError as e:
        raise OperationalError("No se pudo actualizar el usuario", e)


@db_session()
def search_user(db, name: str):
    """Busca un usuario en la base de datos por su nombre.
    Args:
        name (str): Nombre del usuario a buscar.
    Returns:
        db.User: El usuario correspondiente al nombre dado.
    Raises:
        ObjectNotFound: Si no se encuentra al usuario en la base de datos.
        OperationalError: Si no se puede obtener el usuario
    """
    try:
        return db.User[name]
    except OrmError as e:
        raise OperationalError("No se pudo obtener el usuario", e)


@db_session
def check_user(db, username: str) -> bool:
    """Verifica si el usuario existe en la base de datos
    Args:
        username (str): Nombre de usuario
    Returns:
        bool: True si existe, False si no existe
    Raises:
        OperationalError: Si no se puede obtener el usuario
    """
    try:
        return exists(u for u in db.User if u.username == username)
    except OrmError as e:
        raise OperationalError("No se pudo verificar el nombre de usuario", e)


@db_session
def check_email(db, email: str):
    """Verifica si el email existe en la base de datos
    Args:
        email (str): Email del usuario
    Returns:
        bool: True si existe, False si no existe
    Raises:
        OperationalError: Si no se puede obtener el usuario
    """
    try:
        return exists(u for u in db.User if u.email == email)
    except OrmError as e:
        raise OperationalError("No se pudo verificar el email", e)
