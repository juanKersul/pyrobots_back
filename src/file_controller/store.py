from fastapi import UploadFile
from shutil import copyfileobj
from os import mkdir
from exceptions.classes import OperationalError


def save_file(file: UploadFile, new_name: str, destination: str) -> None:
    file.filename = new_name
    try:
        with open(destination + new_name, "wb") as buffer:
            copyfileobj(file.file, buffer)
    finally:
        file.file.close()


def create_directory(path: str) -> None:
    try:
        mkdir(path)
    except OSError:
        raise OperationalError("failed to create directory")
