from pony.orm import Database
from db.entities import define_matches
from db.entities import define_robots
from db.entities import define_users


def define_database():
    """Define la base de datos y crea las tablas
    Args:
        db_params (dict): Parametros de la base de datos"""
    db = Database()
    define_matches(db)
    define_robots(db)
    define_users(db)
    return db


database = define_database()


def map_database(db, **db_params):
    db.bind(**db_params)
    db.generate_mapping(create_tables=True)
