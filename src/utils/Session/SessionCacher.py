default_users_path = "data/users.csv"
default_ships_path = "data/ships.csv"
default_weaponry_path = "data/weaponry.csv"

def create_cache() -> dict:
    cache = {}

    cache["users_path"] = default_users_path
    cache["default_ships_path"] = default_ships_path
    cache["default_weaponry_path"] = default_weaponry_path

    return cache