from pony.orm import db_session
from pony.orm import commit
from exceptions.classes import OperationalError
from exceptions.classes import ObjectNotFound


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
    if User.exists(username=new_username):
        raise OperationalError("El usuario ya existe")
    if User.exists(email=new_email):
        raise OperationalError("El email ya esta en uso")
    User(
        username=new_username,
        password=new_password_encripted,
        confirmation_mail=False,
        email=new_email,
        validation_code=validation_code,
    )
    commit()


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
    if User.exists(username=username) is False:
        raise ObjectNotFound("No existe el usuario con el nombre " + username)
    else:
        user = User[username]
        if user.validation_code == validation_code:
            user.confirmation_mail = True
        else:
            raise OperationalError("Codigo de validacion incorrecto")
        commit()


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
    if User.exists(username=name) is False:
        raise ObjectNotFound("No existe el usuario con el nombre " + name)
    else:
        return User[name]


@db_session
def check_user(username: str):
    """Verifica si el usuario existe en la base de datos
    Args:
        username (str): Nombre de usuario
    Returns:
        bool: True si existe, False si no existe
    Raises:
        OperationalError: Si no se puede obtener el usuario
    """
    return User.exists(username)
