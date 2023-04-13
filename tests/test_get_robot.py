from fastapi.testclient import TestClient
import main
from crud.robot_service import db_session, User, Robot, UploadFile
import os

client = TestClient(main.app)


def client_post_register(username, password, email):
    return client.post(
        "/register", json={"username": username, "password": password, "email": email}
    )


def client_post_robot(files_up: UploadFile, iname: str, itkn: str, iusername: str):
    return client.post(
        "/upload/robot",
        params={
            "name": iname,
            "tkn": itkn,
            "username": iusername,
        },
        files=files_up,
    )


@db_session
def client_fast_confirmation(username: str):
    with db_session:
        User[username].confirmation_mail = True


def test_robot_get_success():
    """
    TEST_1: Listar un robot.
        PRE: Estar logeado.
    """
    client_post_register("Alexis", "Asd23asdasdasdasd@", "ale@gmail.com")
    client_fast_confirmation("Alexis")
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    files_up = [
        ("config", open("tests/test_files/robot1.py", "rb")),
        ("avatar", open("tests/test_files/tortuga.jpg", "rb")),
    ]
    toq_var = response.json()["token"]
    client_post_robot(
        files_up,
        "robot1",
        toq_var,
        "Alexis",
    )

    response = client.get(
        "/robots",
        params={
            "token": toq_var,
        },
    )
    assert len(response.json()) == 1
    delete_db("Alexis")


def test_robot_get_success():
    """
    TEST_2: Pasa mal el token.
        PRE: Estar logeado.
    """
    client_post_register("Alexis", "Asd23asdasdasdasd@", "ale@gmail.com")
    client_fast_confirmation("Alexis")
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    files_up = [
        ("config", open("tests/test_files/robot1.py", "rb")),
        ("avatar", open("tests/test_files/tortuga.jpg", "rb")),
    ]
    toq_var = response.json()["token"]
    client_post_robot(
        files_up,
        "robot1",
        toq_var,
        "Alexis",
    )

    response = client.get(
        "/robots",
        params={
            "token": toq_var + "1",
        },
    )
    assert response.json() == {"detail": "No autorizado, debe logearse"}
    delete_db("Alexis")
