from pony.orm import db_session
from src.db.database import define_database
from src.crud.user_services import add_user
from src.db.entities import User

define_database(provider="sqlite", filename=":memory:", create_db=True)


@db_session
def test_add_user():
    add_user("test", "test", "test", "test")
    assert User.get(username="test")
    assert User.get(password="test")
    assert User.get(email="test")
    assert User.get(validation_code="test")
