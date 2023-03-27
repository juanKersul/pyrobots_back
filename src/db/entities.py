from pony.orm import PrimaryKey, Required, Optional, Set, IntArray


def define_entities(db):
    """Define las entidades de la base de datos."""
    class User(db.Entity):
        """Crea la tabla de usuarios."""

        __table__ = "users"
        username = PrimaryKey(str, 40)
        password = Required(str, 200)
        avatar = Optional(str, nullable=False)
        confirmation_mail = Required(bool)
        email = Required(str, unique=True)
        robots = Set("Robot")
        matchs = Set("Match", reverse="users")
        match_creates = Set("Match", reverse="user_creator")
        validation_code = Required(str, 6)

    class Robot(db.Entity):
        """Crea la tabla de robots."""

        __table__ = "robots"
        id = PrimaryKey(int, auto=True)
        name = Required(str, unique=True)
        avatar = Optional(str)
        matchs_pleyed = Required(int)
        matchs_won = Required(int)
        avg_life_time = Optional(float)
        user_owner = Required(User)

    class Match(db.Entity):
        """Crea la tabla de partidas."""

        id = PrimaryKey(int, auto=True)
        name = Required(str, unique=True)
        max_players = Optional(int)
        min_players = Optional(int)
        password = Optional(str)
        n_matchs = Optional(int)
        n_rounds_matchs = Optional(int)
        users = Set("User", reverse="matchs")
        user_creator = Required(User, reverse="match_creates")
        robots_in_match = Optional(IntArray)
