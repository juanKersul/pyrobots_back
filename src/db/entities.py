from pony import orm
from src.db.database import db


class User(db.Entity):
    """Crea la tabla de usuarios."""
    __tablename__ = "users"
    username = orm.PrimaryKey(str, 40)
    password = orm.Required(str, 200)
    confirmation_mail = orm.Required(bool)
    email = orm.Required(str, unique=True)
    robots = orm.Set("Robot")
    validation_code = orm.Required(str, 6)
    matches = orm.Set("Match", reverse="users")
    match_created = orm.Set("Match", reverse="user_creator")


class Robot(db.Entity):
    """Crea la tabla de robots."""
    __tablename__ = "robots"
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str, unique=True)
    matches_played = orm.Required(int)
    matches_won = orm.Required(int)
    avg_life_time = orm.Optional(float)
    user_owner = orm.Required(User)
    matches = orm.Set("Match")


class Match(db.Entity):
    """Crea la tabla de partidas."""
    id = orm.PrimaryKey(int, auto=True)
    max_players = orm.Required(int)
    password = orm.Optional(str)
    n_matches = orm.Required(int)
    n_rounds = orm.Required(int)
    users = orm.Set("User", reverse="matches")
    user_creator = orm.Required(User)
    robots_in_match = orm.Set("Robot")
