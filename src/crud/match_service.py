from pony.orm import db_session, commit, select
from schemas import imatch
from db.entities import Match, User, Robot
from security.password import encrypt_password


@db_session
def create_match(
    user_creator: str,
    max_players: int,
    match_name: str,
    min_players: int,
    password: str,
    n_matchs: int,
    n_rounds: int,
):
    """Crea una partida en la base de datos."""
    with db_session:
        try:
            Match(
                name=match_name,
                max_players=abs(max_players),
                min_players=abs(min_players),
                password=encrypt_password(password),
                n_matchs=min(abs(n_matchs), 200),
                n_rounds_matchs=min(abs(n_rounds), 10000),
                users={user_creator},
                user_creator=user_creator,
            )
            commit()
        except Exception as e:
            return str(e)
    return "added"


@db_session
def read_matchs():
    """Listar Partidas

    Args:
        token (str): token

    Returns:
        str: En caso de error
        List[Match]: Lista de partidas.
    """
    with db_session:
        try:
            matchs = select(x for x in Match)[:]
            result = [
                {
                    "id": p.id,
                    "name": p.name,
                    "max_players": p.max_players,
                    "min_players": p.min_players,
                    "n_matchs": p.n_matchs,
                    "n_rounds_matchs": p.n_rounds_matchs,
                    "user_creator": p.user_creator.username
                    + ":"
                    + p.user_creator.email,
                }
                for p in matchs
            ]
            commit()
        except Exception as e:
            return str(e)
    return result


@db_session
def read_match(id_match: int):
    with db_session:
        try:
            match = Match[id_match]
            result = imatch.Match.from_orm(match)
            commit()
        except Exception as e:
            return str(e)
        return result


@db_session
def get_match_id(match_name: str):
    result = select(m.id for m in Match if m.name == match_name)
    for i in result:
        return i


@db_session
def get_match_max_players(match_id: int):
    query = select(m.max_players for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def get_match_min_players(match_id: int):
    query = select(m.min_players for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def get_match_rounds(match_id: int):
    query = select(m.n_rounds_matchs for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def get_match_games(match_id: int):
    query = select(m.n_matchs for m in Match if m.id == match_id)
    for i in query:
        result = i
    return result


@db_session
def read_match_players(id_match: int):
    str_result = []
    with db_session:
        result = select(m.users for m in Match if m.id == id_match)
        for i in result:
            str_result.append(i.username)
        return str_result


@db_session
def read_player_in_game(username: str, id_match: int):
    result = select(m.users for m in Match if m.id == id_match)

    return username in result


@db_session
def add_player(id_match: int, id_robot: int, username: str):
    result = ""
    with db_session:
        try:
            match = Match[id_match]
            user = User[username]
            robot = Robot[id_robot]
            if (
                match.user_creator == user
                and len(match.robots_in_match) == 0
                and str(robot.name).split("_")[1] == username
            ):
                list_robots = match.robots_in_match
                list_robots.append(id_robot)
                match.robots_in_match = list_robots
                return str(username) + ":" + str(robot.name).split("_")[0]
            if len(match.users) == match.max_players:
                error = "La partida esta llena"
            elif str(robot.name).split("_")[1] != username:
                error = "El robot no pertenece al usuario"
            elif user in match.users:
                error = "El usuario ya esta en la partida"
        except Exception as e:
            if "Match" in str(e):
                error = "La partida no existe"
            elif "User" in str(e):
                error = "El usuario no existe"
            elif "Robot" in str(e):
                error = "El robot no existe"
            return error
        if error == "":
            match.users.add(user)
            list_robots = match.robots_in_match
            list_robots.append(id_robot)
            match.robots_in_match = list_robots
            result = str(username) + ":" + str(robot.name).split("_")[0]
        else:
            result = error
    return result


@db_session
def remove_player(id_match: int, id_robot: int, name_user: str):
    with db_session:
        try:
            result = "Dejo la partida"
            match = Match[id_match]
            user = User[name_user]
            in_match = match.robots_in_match
            in_match.remove(id_robot)
            match.robots_in_match = in_match
            match.users.remove(user)
        except Exception as e:
            error = ""
            if "Match" in str(e):
                error = "La partida no existe"
            elif "User" in str(e):
                error = "El usuario no existe"
            return error
        return result


@db_session
def start_game(id_match: int, name_user: str):
    with db_session:
        try:
            msg = ""
            match = Match[id_match]
            user = User[name_user]
            if not user.username == match.user_creator.username:
                msg = {"Status": "No es el creador de la partida"}
                return msg
            match_robots = match.robots_in_match
            if (len(match_robots) < get_match_min_players(id_match)) or (
                len(match_robots) > get_match_max_players(id_match)
            ):
                msg = {"ObjectNotFound"}
                return msg
        except Exception as e:
            error = ""
            if "Match" in str(e):
                error = {"Status": "La partida no existe"}
            elif "User" in str(e):
                error = {"Status": "El usuario no existe"}
            return error
    return list(match_robots)


@db_session
def delete_match(id_match: int):
    with db_session:
        try:
            Match[id_match].delete()
        except Exception as e:
            return str(e)
