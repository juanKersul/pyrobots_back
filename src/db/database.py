from pony.orm import Database
from db.entities import define_entities


def define_database(**db_params):
    db = Database()
    define_entities(db)
    db.bind(**db_params)
    db.generate_mapping(create_tables=True)
    return db


db = define_database(provider='sqlite',
                     filename='database.sqlite', create_db=True)