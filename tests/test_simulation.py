from random import randint, uniform
from requests import delete
from fastapi.testclient import TestClient
import main
from crud.user_services import *
from crud.simulation_service import *
import pytest


client = TestClient(main.app)


# Funciones auxiliares para los test
def client_post_register(username, password, email):
    return client.post(
        "/register", json={"username": username, "password": password, "email": email}
    )


@db_session
def elim_user(username: str):
    with db_session:
        User[username].delete()


@db_session
def elim_robots():
    with db_session:
        for i in range(5):
            index = get_robot_id("test_robot_" + str(i))
            Robot[index].delete()


@db_session
def client_fast_confirmation(username: str):
    with db_session:
        User[username].confirmation_mail = True


@db_session
def client_add_robots(username: str):
    with db_session:
        try:
            for i in range(5):
                Robot(
                    name="test_robot_" + str(i),
                    avatar="test_pic_" + str(i),
                    matchs_pleyed=randint(1, 1000),
                    matchs_won=1000 - randint(1, 1000),
                    avg_life_time=uniform(1.1, 100.9),
                    user_owner=username,
                )
                commit()
        except Exception as e:
            return str(e)
        return "added"


def delete_db():
    elim_user("Alexis")


def delete_db_v2():
    elim_robots()


# Tests de partidas
def test_simulation_add_bad_robot():
    """
    TEST_1: Agregar partida incorrectamente,
    sobrepasando el número máximo de robots
    devuelve un error de 422.
    """
    client_post_register("Alexis", "Asd23asdasdasdasd@", "ale@gmail.com")
    client_fast_confirmation("Alexis")
    client_add_robots("Alexis")
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    num_rondas = randint(2, 10000)
    toq_var = response.json()["token"]
    robots = []
    for i in range(5):
        robots.append(get_robot_id("test_robot_" + str(i)))
    response = client.post(
        "/simulation/add",
        json={
            "id_robot": ""
            + str(robots[0])
            + ","
            + str(robots[1])
            + ","
            + str(robots[2])
            + ","
            + str(robots[3])
            + ","
            + str(robots[4])
            + "",
            "n_rounds_simulations": num_rondas,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    delete_db()
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "id_robot"],
                "msg": "El valor debe estar entre 2 y 4",
                "type": "value_error",
            }
        ]
    }


def test_simulation_add_bad_robot_v2():
    """
    TEST_2: Agregar partida incorrectamente,
    sobrepasando el número mínimo de robots
    devuelve un error de 422.
    """
    client_post_register("Alexis", "Asd23asdasdasdasd@", "ale@gmail.com")
    client_fast_confirmation("Alexis")
    client_add_robots("Alexis")
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    num_rondas = randint(2, 10000)
    toq_var = response.json()["token"]
    robots = []
    for i in range(5):
        robots.append(get_robot_id("test_robot_" + str(i)))
    response = client.post(
        "/simulation/add",
        json={
            "id_robot": "" + str(robots[0]) + "",
            "n_rounds_simulations": num_rondas,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    delete_db()
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "id_robot"],
                "msg": "El valor debe estar entre 2 y 4",
                "type": "value_error",
            }
        ]
    }


def test_simulation_empty_robot():
    """
    TEST_3: Agregar partida incorrectamente,
    pasando lista vacía de robots.
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
    num_rondas = randint(2, 10000)
    toq_var = response.json()["token"]
    response = client.post(
        "/simulation/add",
        json={
            "id_robot": "",
            "n_rounds_simulations": num_rondas,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    delete_db()
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "id_robot"],
                "msg": "El valor debe estar entre 2 y 4",
                "type": "value_error",
            }
        ]
    }


def test_simulation_wrong_format():
    """
    TEST_4: Agregar partida incorrectamente,
    pasando la lista de robots con formato incorrecto.
    """
    client_post_register("Alexis", "Asd23asdasdasdasd@", "ale@gmail.com")
    client_fast_confirmation("Alexis")
    client_add_robots("Alexis")
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    num_rondas = randint(2, 10000)
    toq_var = response.json()["token"]
    robots = []
    for i in range(5):
        robots.append(get_robot_id("test_robot_" + str(i)))
    response = client.post(
        "/simulation/add",
        json={
            "id_robot": ""
            + str(robots[0])
            + ", "
            + str(robots[1])
            + ", "
            + str(robots[2])
            + " ",
            "n_rounds_simulations": num_rondas,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    delete_db()
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "id_robot"],
                "msg": "La lista de robots no puede contener caracteres vacíos",
                "type": "value_error",
            }
        ]
    }


def test_simulation_wrong_rounds():
    """
    TEST_5: Crear una simulacion con mas rondas de las posibles
    devuelve un error de 422.
    """
    client_post_register("Alexis", "Asd23asdasdasdasd@", "ale@gmail.com")
    client_fast_confirmation("Alexis")
    client_add_robots("Alexis")
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    robots = []
    for i in range(5):
        robots.append(get_robot_id("test_robot_" + str(i)))
    response = client.post(
        "/simulation/add",
        json={
            "id_robot": ""
            + str(robots[0])
            + ","
            + str(robots[1])
            + ","
            + str(robots[2])
            + "",
            "n_rounds_simulations": 10001,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    delete_db()
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "n_rounds_simulations"],
                "msg": "El valor debe estar entre 2 y 10.000",
                "type": "value_error",
            }
        ]
    }


def test_simulation_wrong_rounds_v2():
    """
    TEST_5: Crear una simulacion con menos rondas de las posibles
    devuelve un error de 422.
    """
    client_post_register("Alexis", "Asd23asdasdasdasd@", "ale@gmail.com")
    client_fast_confirmation("Alexis")
    client_add_robots("Alexis")
    response = client.post(
        "/login",
        json={
            "username": "Alexis",
            "email": "ale@gmail.com",
            "password": "Asd23asdasdasdasd@",
        },
    )
    toq_var = response.json()["token"]
    robots = []
    for i in range(5):
        robots.append(get_robot_id("test_robot_" + str(i)))
    response = client.post(
        "/simulation/add",
        json={
            "id_robot": ""
            + str(robots[0])
            + ","
            + str(robots[1])
            + ","
            + str(robots[2])
            + "",
            "n_rounds_simulations": 1,
            "user_creator": "Alexis",
            "token": toq_var,
        },
    )
    delete_db()
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "n_rounds_simulations"],
                "msg": "El valor debe estar entre 2 y 10.000",
                "type": "value_error",
            }
        ]
    }
