from pony.orm import Database

db = Database()


def define_database(**db_params):
    """Define la base de datos y crea las tablas
    Args:
        db_params (dict): Parametros de la base de datos"""
    db.bind(**db_params)
    db.generate_mapping(create_tables=True)
