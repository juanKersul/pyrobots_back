from fastapi import UploadFile
from shutil import copyfileobj


def save_file(file: UploadFile, new_name: str, destination: str) -> None:
    file.filename = new_name
    try:
        with open(destination + new_name, "wb") as buffer:
            copyfileobj(file.file, buffer)
    finally:
        file.file.close()


def generate_key(str1: str, str2: str) -> str:
    """Genera una clave para unir dos strings

    Args:
        str1 (str): string 1
        str2 (str): string 2

    Returns:
        str: clave
    """
    return str(hash(str1 + " " + str2))
