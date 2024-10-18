default_users_path = ""
default_ships_path = ""

def create_cache() -> dict:
    cache = {}

    cache["users_path"] = default_users_path
    cache["default_ships_path"] = default_ships_path

    return cache