import utils.fileUtils.CsvUtils as CsvUtils
from Session import Session

def create_account(account_login: str, password, users_path: str):
    users = CsvUtils.get_csv_values_with_key(users_path, main_key="login")
    user_data = {}

    if users.__contains__(account_login):
        # Push warning
        print("WARNING: User is already in the database!")
        return user_data

    # Add to session cache and save on database

    return user_data

def log_in(account_login: str, password: str, users_path: str) -> dict:
    users = CsvUtils.get_csv_values_with_key(users_path, main_key="login")
    user_data = {}

    if not users.__contains__(account_login):
        # Push warning
        print("WARNING: Couldn't find user in database!")
        return user_data

    if users[account_login]["password"] != password:
        # Push warning
        print("WARNING: Wrong password")
        return user_data
    
    user_data = users[account_login]

    return user_data
