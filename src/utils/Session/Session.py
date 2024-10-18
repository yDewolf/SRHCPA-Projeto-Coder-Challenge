import SessionCacher

class Session:
    user_data: dict
    logged_in: bool = False
    cache: dict

    def __init__(self, user_data: dict, cache: dict) -> None:
        self.user_data = user_data
        self.cache = SessionCacher.create_cache()
    
    def log_in(self, user_data: dict):
        self.user_data = user_data
        self.logged_in = True