from pony.orm import db_session
from pony.orm import commit
from pony.orm import rollback
from pony.orm import ObjectNotFound
from pony.orm import OperationalError
from db.entities import User


@db_session()
def add_user(
    new_username: str,
    new_password_encripted: str,
    new_email: str,
    validation_code: str
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
        User(
            username=new_username,
            password=new_password_encripted,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        commit()
    except OperationalError("no se pudo agregar el usuario"):
        rollback()
        raise


@db_session
def update_confirmation(username: str, validation_code: str):
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
        user = User.get(username=username, validation_code=validation_code)
    except OperationalError("no se pudo obtener el usuario"):
        raise
    if user:
        try:
            user.confirmation_mail = True
            commit()
        except OperationalError("no se pudo actualizar el usuario"):
            rollback()
            raise
    else:
        raise ObjectNotFound("No existe el usuario con el nombre " + username)


@db_session()
def search_user(name: str):
    """ Busca un usuario en la base de datos por su nombre.
    Args:
        name (str): Nombre del usuario a buscar.
    Returns:
        User: El usuario correspondiente al nombre dado.
    Raises:
        ObjectNotFound: Si no se encuentra al usuario en la base de datos.
        OperationalError: Si no se puede obtener el usuario
    """
    try:
        user = User.get(username=name)
    except OperationalError("no se pudo obtener el usuario"):
        raise
    if user is None:
        raise ObjectNotFound("No existe el usuario con el nombre " + name)
    else:
        return user
