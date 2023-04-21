import sys
path = "src"
sys.path.append(path)
from src.crud.match_service import create_match
from src.exceptions.classes import ObjectNotFound
from pony.orm import db_session
from src.db.database import define_database
from src.db.database import map_database
from src.exceptions.classes import OperationalError
from src.exceptions.classes import ObjectNotFound
import pytest

db = define_database()


class TestCreateMatch:
    @classmethod
    def setup_class(cls):
        map_database(db, provider="sqlite", filename=":memory:", create_db=False)

    @classmethod
    def teardown_class(cls):
        db.drop_all_tables(with_all_data=True)
        db.disconnect()

    @db_session
    def test_user_creator_exists_in_db(self):
        # Happy path test
        """Test that a match is successfully created when the user_creator
        exists in the database"""
        new_username = "test_user"
        new_password = "test_password"
        new_email = "test_email@test.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        result = create_match(
            db,
            user_creator=new_username,
            max_players=4,
            password="test_password",
            max_matches=3,
            max_rounds=5,
        )
        db.rollback()
        assert isinstance(result, int)
        assert db.Match[result].user_creator.username == new_username

    @db_session
    def test_function_returns_match_primary_key(self):
        # Happy path test
        """Test that the function returns the primary key of the created
        match"""
        new_username = "test_user2"
        new_password = "test_password"
        new_email = "test_email@test2.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        db.commit()
        result = create_match(
            db,
            user_creator=new_username,
            max_players=4,
            password="test_password",
            max_matches=3,
            max_rounds=5,
        )
        assert result == db.Match[result].id
        assert db.Match[result].user_creator.username == new_username
        

    def test_user_creator_does_not_exist_in_db(self):
        # Edge case test
        """Test that ObjectNotFound is raised when the user_creator does not
        exist in the database"""
        with pytest.raises(Exception) as e:
            create_match(
                db,
                user_creator="non_existing_user",
                max_players=4,
                password="test_password",
                max_matches=3,
                max_rounds=5,
            )
            assert e is ObjectNotFound

    @db_session
    def test_match_creation_fails(self):
        # Edge case test
        """Test that OperationalError is raised when match creation fails"""
        new_username = "test_user3"
        new_password = "test_password"
        new_email = "test_email@test3.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        db.commit()
        with pytest.raises(Exception) as e:
            create_match(
                db,
                user_creator=new_username,
                max_players=0,
                password="test_password",
                max_matches=3,
                max_rounds=5,
            )
            assert e is OperationalError

    def test_function_raises_ObjectNotFound_if_user_creator_not_found(self):
        # Edge case test
        """Test that ObjectNotFound is raised when the user_creator is
        not found"""
        with pytest.raises(Exception) as e:
            create_match(
                db,
                user_creator="non_existing_user",
                max_players=4,
                password="test_password",
                max_matches=3,
                max_rounds=5,
            )
            assert e is ObjectNotFound

    def test_function_raises_OperationalError_if_user_search_fails(self):
        # Edge case test
        """Test that ObjectNotFound is raised when user search fails"""
        with pytest.raises(Exception) as e:
            create_match(
                db,
                user_creator="non_existing_user",
                max_players=4,
                password="test_password",
                max_matches=3,
                max_rounds=5,
            )
            assert e is ObjectNotFound

    @db_session
    def test_function_raises_OperationalError_if_match_creation_fails(self):
        # Edge case test
        """Test that OperationalError is raised when match creation fails"""
        new_username = "test_user10"
        new_password = "test_password"
        new_email = "test_email@test10.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        db.commit()
        with pytest.raises(Exception) as e:
            create_match(
                db,
                user_creator=new_username,
                max_players=-1,
                password="test_password",
                max_matches=3,
                max_rounds=5,
            )
            assert e is OperationalError

    @db_session
    def test_max_players_input_value(self):
        # Edge case test
        """Test the function with different input values for max_players"""
        new_username = "test_user4"
        new_password = "test_password"
        new_email = "test_email@test4.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        db.commit()
        with pytest.raises(Exception) as e:
            create_match(
                db,
                user_creator=new_username,
                max_players=-1,
                password="test_password",
                max_matches=3,
                max_rounds=5,
            )
            assert e is OperationalError

    @db_session
    def test_password_input_value(self):
        # Edge case test
        """Test the function with different input values for password"""
        new_username = "test_user5"
        new_password = "test_password"
        new_email = "test_email@test5.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        db.commit()
        match = create_match(
            db,
            user_creator=new_username,
            password=None,
            max_players=4,
            max_matches=3,
            max_rounds=5,
        )
        assert match is not None

    @db_session
    def test_max_matches_input_value(self):
        # Edge case test
        """Test the function with different input values for max_matches"""
        new_username = "test_user6"
        new_password = "test_password"
        new_email = "test_email@test6.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        db.commit()
        with pytest.raises(Exception) as e:
            create_match(
                db,
                user_creator=new_username,
                max_players=4,
                password="test_password",
                max_matches=-1,
                max_rounds=5,
            )
            assert e is OperationalError

    @db_session
    def test_max_rounds_input_value(self):
        # Edge case test
        """Test the function with different input values for max_rounds"""
        new_username = "test_user7"
        new_password = "test_password"
        new_email = "test_email@test7.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        db.commit()
        with pytest.raises(Exception) as e:
            create_match(
                db,
                user_creator=new_username,
                max_players=4,
                password="test_password",
                max_matches=3,
                max_rounds=-1,
            )
            assert e is OperationalError

    @db_session
    def test_same_user_creator_values(self):
        # Edge case test
        """Test the function with different user_creator values"""
        new_username = "test_user9"
        new_password = "test_password"
        new_email = "test_email@test9.com"
        validation_code = "1234"
        db.User(
            username=new_username,
            password=new_password,
            confirmation_mail=False,
            email=new_email,
            validation_code=validation_code,
        )
        db.commit()
        match1 = create_match(
            db,
            max_players=4,
            password="test_password",
            max_matches=3,
            max_rounds=5,
            user_creator=new_username,
        )
        match2 = create_match(
            db,
            max_players=4,
            password="test_password",
            max_matches=3,
            max_rounds=5,
            user_creator=new_username,
        )
        assert match1 is not None
        assert match2 is not None
        assert match1 != match2
