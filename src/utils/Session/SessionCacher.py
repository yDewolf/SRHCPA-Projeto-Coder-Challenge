default_users_path = "data/users.csv"
default_ships_path = "data/ships.csv"
default_ship_models_path = "data/ship_models.csv"
default_weaponry_path = "data/weaponry.csv"

def create_cache() -> dict:
    cache = {}

    cache["users_path"] = default_users_path
    cache["ships_path"] = default_ships_path
    cache["ship_models_path"] = default_ship_models_path
    cache["weaponry_path"] = default_weaponry_path

    return cache