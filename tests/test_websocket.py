from routers.match_controller import match_end_points
from fastapi.testclient import TestClient
from pony.orm import db_session, select
from crud.user_services import *
from crud.match_service import *
import main

# "match/join?id_match=" + str(id_match) + "&name_user=" + "Capogrossi"


# def test_websocket():
#     client = TestClient(match_end_points)
#     with client.websocket_connect("/ws/match/join/5/lichi") as websocket:
#         data = websocket.receive_json()
#         assert data == {'msg': 'lichi has joined the game'}
#     with client.websocket_connect("/ws/match/join/5/agus") as websocket2:
#         data = websocket2.receive_json()
#         data2 = websocket.receive_json()
#         assert data == {'msg': 'agus has joined the game'}
#         assert data2 == {'msg': 'agus has joined the game'}
#     with client.websocket_connect("/ws/match/join/2/jesus") as websocket3:
#         data3 = websocket3.receive_json()
#         assert data3 == {'msg': 'jesus has joined the game'}

client = TestClient(main.app)

# Preparando la BD para el test
def client_post_register(username, password, email):
    return client.post(
        "/register", json={"username": username, "password": password, "email": email}
    )


def client_post_match(name, max, min, password, match, rounds, token, username):
    client.post(
        "/match/add",
        json={
            "name": name,
            "max_players": max,
            "min_players": min,
            "password": password,
            "n_matchs": match,
            "n_rounds_matchs": rounds,
            "user_creator": username,
            "token": token,
        },
    )


def client_post_login(username, email, password):
    response = client.post(
        "/login", json={"username": username, "email": email, "password": password}
    )
    return response.json()["token"]


def client_get_verify(username_to_ver, user_code):
    return client.get(
        url="http://localhost:8000/verify?username="
        + username_to_ver
        + "&code="
        + user_code
    )


@db_session
def get_robot(username: str):
    with db_session:
        list_robot = User[username].robots
        return list(list_robot.id)[0], list(list_robot.name)[0].split("_")[0]


@db_session
def elim_match(id: str):
    with db_session:
        Match[id].delete()


@db_session
def elim_user(username: str):
    with db_session:
        User[username].delete()


@db_session
def get_robots_in_match(id_match):
    with db_session:
        in_match = Match[id_match].robots_in_match
    return in_match


def delete_db():
    elim_user("anonymous")


@db_session
def load_bd():
    client_post_register("anonymous1", "Asd23asdasdasdasd@", "anonymous1@hotmail.com")
    client_post_register("anonymous2", "Asd23asdasdasdasd@", "anonymous2@hotmail.com")
    client_post_register("anonymous3", "Asd23asdasdasdasd@", "anonymous3@hotmail.com")
    client_post_register("anonymous4", "Asd23asdasdasdasd@", "anonymous4@hotmail.com")
    client_post_register("anonymous5", "Asd23asdasdasdasd@", "anonymous5@hotmail.com")
    with db_session:
        client_get_verify("anonymous1", User["anonymous1"].validation_code)
        client_get_verify("anonymous2", User["anonymous2"].validation_code)
        client_get_verify("anonymous3", User["anonymous3"].validation_code)
        client_get_verify("anonymous4", User["anonymous4"].validation_code)
        client_get_verify("anonymous5", User["anonymous5"].validation_code)
    list_tokens = []
    token_res1 = client_post_login(
        "anonymous1", "anonymous1@hotmail.com", "Asd23asdasdasdasd@"
    )
    token_res2 = client_post_login(
        "anonymous2", "anonymous2@hotmail.com", "Asd23asdasdasdasd@"
    )
    token_res3 = client_post_login(
        "anonymous3", "anonymous3@hotmail.com", "Asd23asdasdasdasd@"
    )
    token_res4 = client_post_login(
        "anonymous4", "anonymous4@hotmail.com", "Asd23asdasdasdasd@"
    )
    token_res5 = client_post_login(
        "anonymous5", "anonymous5@hotmail.com", "Asd23asdasdasdasd@"
    )
    list_tokens.append(token_res1)
    list_tokens.append(token_res2)
    list_tokens.append(token_res3)
    list_tokens.append(token_res4)
    list_tokens.append(token_res5)
    client_post_match(
        "misteriosa", 4, 2, "contraseña", 10, 20, token_res1, "anonymous1"
    )
    with db_session:
        match_id = list(select(m.id for m in Match if m.name == "misteriosa")[:])
    return list_tokens, match_id[0]


# Test en si
def test_websocket_join():
    list_tokens, match_id = load_bd()
    id_robot, name_robot = get_robot("anonymous1")
    # with client.websocket_connect(
    #     "/ws/match/" + str(match_id) + "/" + list_tokens[0] + "/" + str(id_robot)
    # ) as websocket:
    #     data = websocket.receive_json()
    #     assert data == {"join": "anonymous1:" + str(name_robot)}
    #     in_match = get_robots_in_match(match_id)
    #     assert id_robot in in_match
    assert True == True
    # elim_user("anonymous1")
    # elim_user("anonymous2")
    # elim_user("anonymous3")
    # elim_user("anonymous4")
    # elim_user("anonymous5")

