from cryptography.fernet import Fernet
from decouple import config
KEY_CRYPT = config("KEY")

def decrypt_password(password: str):
    """Desencripta una contraseña

    Args:
        password (str): contraseña a desencriptar

    Returns:
        str: contraseña desencriptada
    """
    f = Fernet(KEY_CRYPT)
    encoded_pasword = password.encode()
    decripted_password = f.decrypt(encoded_pasword)
    decoded_password = decripted_password.decode()
    return decoded_password


def encrypt_password(password: str):
    """Realiza un encriptado simetrico a un string haciendo uso de Fernet

    Args:
        password (str): String a encriptar

    Returns:
        _type_: String encriptada
    """
    f = Fernet(KEY_CRYPT)
    encoded_pasword = password.encode()
    encripted_password = f.encrypt(encoded_pasword)
    decoded_password = encripted_password.decode()
    return decoded_password