import pytest
from fastapi.testclient import TestClient
import main
import os
from crud.robot_service import *


client = TestClient(main.app)

@db_session
def elim_user(username: str):
    with db_session:
        User[username].delete()


@db_session
def elim_bot(name: str):
    with db_session:
        id = Robot[name].id
        Robot[id].delete()


def delete_db():
    elim_user("anonymous")
    file_path = os.path.join('routers/robots/', 'robot1_anonymous.py')
    os.remove(file_path)
    file_path2 = os.path.join('routers/robots/', 'robot2_anonymous.py')
    os.remove(file_path2)
    file_path3 = os.path.join('routers/robots/avatars/', 'anonymous_robot1.jpg')
    os.remove(file_path3)

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
def client_fast_confirmation(username: str):
    with db_session:
        User[username].confirmation_mail = True


def test_load_robot():
    client_post_register(
        "anonymous",
        "Asd23asdasdasdasd@",
        "anonymous@hotmail.com"
        )
    client_fast_confirmation("anonymous")
    response = client.post(
        "/login",
        json={
            "username": "anonymous",
            "email": "anonymous@hotmail.com",
            "password": "Asd23asdasdasdasd@"
        },
    )
    usr_tkn = response.json()['token']
    files_up = [("config", open("tests/test_files/robot1.py", "rb")),
                ("avatar", open("tests/test_files/tortuga.jpg", "rb"))]
    response = client.post(
        "/upload/robot",
        params={
            "name": "robot1",
            "tkn": usr_tkn
        },
        files=files_up
    )
    assert response.json()["msg"] == "Robot agregado con exito"

def test_load_robot_no_avatar():
    response = client.post(
        "/login",
        json={
            "username": "anonymous",
            "email": "anonymous@hotmail.com",
            "password": "Asd23asdasdasdasd@"
        },
    )
    usr_tkn = response.json()['token']
    files_up = [("config", open("tests/test_files/robot2.py", "rb"))]
    response = client.post(
        "/upload/robot",
        params={
            "name": "robot2",
            "tkn": usr_tkn
        },
        files=files_up
    )
    assert response.json()["msg"] == "Robot agregado con exito"

def test_load_bad_tkn():
    response = client.post(
        "/login",
        json={
            "username": "anonymous",
            "email": "anonymous@hotmail.com",
            "password": "Asd23asdasdasdasd@"
        },
    )
    usr_tkn = response.json()['token']
    files_up = [("config", open("tests/test_files/robot1.py", "rb")),
                ("avatar", open("tests/test_files/tortuga.jpg", "rb"))]
    response = client.post(
        "/upload/robot",
        params={
            "name": "robot1",
            "tkn": usr_tkn+"____"
        },
        files=files_up
    )
    assert response.json()["detail"] == "Sesión expirada"

def test_load_bad_format():
    response = client.post(
        "/login",
        json={
            "username": "anonymous",
            "email": "anonymous@hotmail.com",
            "password": "Asd23asdasdasdasd@"
        },
    )
    usr_tkn = response.json()['token']
    files_up = [("config", open("tests/test_files/robot1.py", "rb")),
                ("avatar", open("tests/test_files/tortuga.jpg", "rb"))]
    response = client.post(
        "/upload/robot",
        params={
            "name": "robot",
            "tkn": usr_tkn
        },
        files=files_up
    )
    delete_db()
    assert response.json()["detail"] == "El archivo no cumple los requisitos"