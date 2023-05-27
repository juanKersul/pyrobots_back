from pydantic import BaseModel, validator
from typing import Optional
import re


special_chars = "~`!@#$%^&*()-_+={}[]\\|/:;\"'<>,.?"


class User_base(BaseModel):
    username: str
    password: str
    email: str

    @validator("username")
    def username_validator(cls, username):
        if username == "":
            raise ValueError("El usuario no puede ser vacio")
        if " " in username:
            raise ValueError("El nombre de usuario no puede contener espacios")
        if len(username) > 40:
            raise ValueError("El nombre de usuario supera los 40 caracteres")
        return username

    @validator("password")
    def password_validator(cls, password):
        if len(password) < 7:
            raise ValueError("La longitud mínima es de 8 caracteres.")
        if len(password) > 50:
            raise ValueError("La longitud máxima es de 50 caracteres.")
        if password.islower() or password.isupper():
            raise ValueError("Debe contener al menos una mayuscula y una minuscula")
        if " " in password:
            raise ValueError("No debe contener espacios")
        if not (re.search(r"\d", password)):
            raise ValueError("Debe contener al menos un numero")
        if not any(c in special_chars for c in password):
            raise ValueError("Debe contener al menos un caracter especial")
        return password

    @validator("email")
    def email_validator(cls, email):
        regex = (
            r"[a-zA-Z0-9_.-]+[^!#$%^&*()]@(?:gmail"
            r"|hotmail|yahoo|live|mi.unc|outlook)\.(?:com|es|edu.ar)"
        )
        if not re.search(regex, email):
            raise ValueError("Email invalido")
        return email


class User_create(User_base):
    class Config:
        orm_mode = True


class User_login_schema(BaseModel):
    username: str
    email: str
    password: str
