from pony.orm import Database
from entities import define_entities


def define_database(**db_params):
    db = Database(**db_params)
    define_entities(db)
    db.generate_mapping(create_tables=True)
    return db
