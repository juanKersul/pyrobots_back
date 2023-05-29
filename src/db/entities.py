from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Set
from pony.orm import Optional


def define_users(db):
    class User(db.Entity):
        """Crea la tabla de usuarios."""

        __tablename__ = "users"
        username = PrimaryKey(str, 40)
        password = Required(str, 200)
        confirmation_mail = Required(bool)
        email = Required(str, unique=True)
        robots = Set("Robot")
        validation_code = Required(str, 6)
        matches = Set("Match", reverse="users")
        match_created = Set("Match", reverse="user_creator")

    return User


def define_robots(db):
    class Robot(db.Entity):
        """Crea la tabla de robots."""

        __tablename__ = "robots"
        name = Required(str)
        user_owner = Required("User")
        PrimaryKey(name, user_owner)
        matches_played = Required(int)
        matches_won = Required(int)
        avg_life_time = Optional(float)
        matches = Set("Match")

    return Robot


def define_matches(db):
    class Match(db.Entity):
        """Crea la tabla de partidas."""

        id = PrimaryKey(int, auto=True)
        max_players = Required(int, unsigned=True)
        password = Optional(str, nullable=True)
        n_rounds = Required(int, unsigned=True)
        users = Set("User", reverse="matches")
        user_creator = Required("User")
        robots_in_match = Set("Robot")
        key = Optional(str, nullable=True)

    return Match
