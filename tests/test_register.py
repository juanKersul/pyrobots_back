import pytest
from fastapi.testclient import TestClient
import main
from crud.user_services import *


client = TestClient(main.app)


# Funciones auxiliares para los test
def client_post_register(username, password, email):
    return client.post(
        "/register",
        json={
            "username": username,
            "password": password,
            "email": email
            }
    )


@db_session
def elim_user(username: str):
    with db_session:
        User[username].delete()


def delete_db():
    elim_user("anonymousRealNoFake")
    elim_user("anonymousReal")
    elim_user("anonymous")


# Test para el registro de usuarios
def test_register_username_success():
    response = client_post_register(
        "anonymous",
        "Asd23asdasdasdasd@",
        "anonymous@hotmail.com"
        )
    assert response.json() == {"Status": "Usuario agregado con exito"}


def test_register_username_repeat():
    response = client_post_register(
        "anonymous",
        "Asd23asdasdasdasd@",
        "anonymous_ok@hotmail.com"
    )
    assert response.json()["detail"] == "El nombre de usuario ya existe"


def test_register_username_empty():
    response = client_post_register(
        "",
        "Asd23asdasdasdasd@",
        "anonymous_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "El usuario no puede ser vacio"


def test_register_username_with_spaces():
    response = client_post_register(
        "asdfañsdjfa                  fajñsldkfja",
        "Asd23asdasdasdasd@",
        "anonymous_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "El nombre de usuario no puede contener espacios"


def test_register_username_full_spaces():
    response = client_post_register(
        "                                 ",
        "Asd23asdasdasdasd@",
        "anonymous_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "El nombre de usuario no puede contener espacios"


def test_register_username_long():
    response = client_post_register(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "Asd23asdasdasdasd@",
        "anonymous_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "El nombre de usuario supera los 40 caracteres"


# Test para la password
def test_register_password_short():
    response = client_post_register(
        "anonymousReal",
        "ano",
        "anonymous_real_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "La longitud mínima es de 8 caracteres."


def test_register_password_no_upper():
    response = client_post_register(
        "anonymousReal",
        "anonymouspass",
        "anonymous_real_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "Debe contener al menos una mayuscula y una minuscula"


def test_register_password_no_lower():
    response = client_post_register(
        "anonymousReal",
        "ANONYMOUSPASS",
        "anonymous_real_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "Debe contener al menos una mayuscula y una minuscula"


def test_register_password_no_num():
    response = client_post_register(
        "anonymousReal",
        "anonymousPass",
        "anonymous_real_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "Debe contener al menos un numero"


def test_register_password_no_special():
    response = client_post_register(
        "anonymousReal",
        "anonymousPass666",
        "anonymous_real_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "Debe contener al menos un caracter especial"


def test_register_password_long():
    response = client_post_register(
        "anonymousReal",
        "an@nymousPass666jajajajajajajajajajajajajajajajajaja",
        "anonymous_real_ok@hotmail.com"
    )
    assert response.json()["detail"][0]["msg"] \
        == "La longitud máxima es de 50 caracteres."


def test_register_password_success():
    response = client_post_register(
        "anonymousReal",
        "an@nymousPass666",
        "anonymous_real_ok@hotmail.com"
    )
    assert response.json() == {"Status": "Usuario agregado con exito"}


# Test para el email
def test_register_email_repeat():
    response = client_post_register(
        "anonymousRealNoFake",
        "an@nymousPass666",
        "anonymous_real_ok@hotmail.com"
    )
    assert response.json() == {"detail": "El email ya existe"}


def test_register_email_error():
    response = client_post_register(
        "anonymousRealNoFake",
        "an@nymousPass666",
        "anonymous_real_ok@jemail.com"
    )
    assert response.json()["detail"][0]["msg"] == "Email invalido"


def test_register_email_success():
    response = client_post_register(
        "anonymousRealNoFake",
        "an@nymousPass666",
        "anonymous_real_ok@mi.unc.edu.ar"
    )
    delete_db()
    assert response.json() == {"Status": "Usuario agregado con exito"}
