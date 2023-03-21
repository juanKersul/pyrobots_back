import pytest
from fastapi.testclient import TestClient
import main
from routers.users_controller import *
from crud.user_services import *
import string
import random
from datetime import datetime


client = TestClient(main.app)


# Cargando la base de datos
def client_post_register_l(username, password, email):
    return client.post(
        "/register",
        json={
            "username": username,
            "password": password,
            "email": email
            }
    )


def test_register_username1_success():
    response = client_post_register_l(
        "juanka",
        "Asd123@",
        "juanka@hotmail.com"
    )
    assert response.json() == {"Status": "Usuario agregado con exito"}


def test_register_username2_success():
    response = client_post_register_l(
        "messi",
        "Antonela@123",
        "messi@hotmail.com")
    assert response.json() == {"Status": "Usuario agregado con exito"}


def test_set_confirmation_true():
    response = set_confirmation_true("juanka")
    assert response == {"exito"}


# Tests para login
def test_username_login_invalid_user():
    response = client.post(
        "/login",
        json={
            "username": "asdsad",
            "email": "aasdasd",
            "password": "asdasdasd"
            }
    )
    assert response.json() == {"detail": "no existe el usuario"}


def test_email_login_invalid_user():
    response = client.post(
        "/login",
        json={
            "username": "",
            "email": "aasdasd",
            "password": "asdasdasd"
            }
    )
    assert response.json() == {"detail": "no existe el usuario"}


def test_user_login_invalid_password():
    response = client.post(
        "/login",
        json={
            "username": "juanka",
            "email": "",
            "password": "asdasdasd"
        }
    )
    assert response.json() == {"detail": "contrasenia incorrecta"}


def test_email_login_invalid_password():
    response = client.post(
        "/login",
        json={
            "username": "",
            "email": "juanka@hotmail.com",
            "password": "asdasdasd"
            }
    )
    assert response.json() == {"detail": "contrasenia incorrecta"}


def test_user_login_email_not_verificated():
    response = client.post(
        "/login",
        json={
            "username": "messi",
            "email": "",
            "password": "Antonela@123"
            }
    )
    assert response.json() == {"detail": "email no verificado"}


def test_email_login_email_not_verificated():
    response = client.post(
        "/login",
        json={
            "username": "",
            "email": "messi@hotmail.com",
            "password": "Antonela@123"
            }
    )
    assert response.json() == {"detail": "email no verificado"}


def test_user_login_success():
    response = client.post(
        "/login",
        json={
            "username": "juanka",
            "email": "",
            "password": "Asd123@"
            }
    )
    assert response.json() != {"detail": "email no verificado"} \
        and response.json() != {"detail": "contrasenia incorrecta"} \
        and response.json() != {"detail": "no existe el usuario"}


def test_email_login_success():
    response = client.post(
        "/login",
        json={
            "username": "",
            "email": "juanka@hotmail.com",
            "password": "Asd123@"
            }
    )
    assert response.json() != {"detail": "email no verificado"} \
        and response.json() != {"detail": "contrasenia incorrecta"} \
        and response.json() != {"detail": "no existe el usuario"}


# Funciones auxiliares para los test
@db_session
def set_confirmation_true(username):
    with db_session:
        user_data = User[username]
        user_data.confirmation_mail = True
        return {"exito"}


length_of_string = 8
random_str = (
    random.choice(string.ascii_letters + string.digits)
    for _ in range(length_of_string)
)


def test_get_payload(userID=random_str):
    assert get_payload(userID)["expiry"] <= str(datetime.now() + JWT_EXPIRES)


random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
token = sign_JWT(random_str)
payload = get_payload(random_str)
decoded_token = decode_JWT(token)


def test_sign_and_decode_JWT(r=random_str):
    assert payload['userID'] == decoded_token['userID']
    delete_db()


@db_session
def elim_user(username: str):
    with db_session:
        User[username].delete()


def delete_db():
    elim_user("juanka")
    elim_user("messi")
