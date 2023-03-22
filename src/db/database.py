from pony.orm import Database

db = Database()
db.bind(provider="sqlite", filename="pyrobots.bd", create_db=True)


def gen_map():
    """
    Asigna las entidades definidas a las tablas de la base de datos
    """
    db.generate_mapping(create_tables=True)
