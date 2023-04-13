from src.crud.user_services import update_confirmation
from fastapi.testclient import TestClient
import main
from crud.user_services import *


client = TestClient(main.app)

# Test para la confirmacion de usuarios
def client_get_verify(username_to_ver, user_code):
    return client.get(
        url="http://localhost:8000/verify?username="
            + username_to_ver + "&code="+user_code
    )


def test_confirmation_success():
    client_post_register(
        "anonymous",
        "Asd23asdasdasdasd@",
        "anonymous@hotmail.com"
    )
    response = client_get_verify(
        username_to_ver="anonymous",
        user_code=get_code_for_user("anonymous")
        )
    assert str(response) ==  "<Response [404]>"
    response = client_get_verify(
        username_to_ver="anonymous",
        user_code=get_code_for_user("anonymous")
        )
    assert str(response) ==  "<Response [404]>"

def test_confirmation_user_wrong():
    user_wrong = "anonymousNotExist"
    response = client_get_verify(
        username_to_ver=user_wrong,
        user_code=get_code_for_user("anonymous")
        )
    assert response.json()["detail"] == "El usuario "+user_wrong+" no existe"


def test_confirmation_code_wrong():
    response = client_get_verify(
        username_to_ver="anonymous",
        user_code="elToken"
        )
    assert response.json()["detail"] \
        == "El codigo de confirmacion no es valido"
    delete_db()
