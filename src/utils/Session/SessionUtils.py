import utils.fileUtils.CsvUtils as CsvUtils
import utils.fileUtils.FileUtils as FileUtils

def create_account(account_login: str, password, users_path: str):
    users = CsvUtils.get_csv_values_with_key(users_path, main_key="login")
    user_data = {}

    if _check_user_exists(account_login, users, push_warning=False):
        # Push Warning:
        print("WARNING: This user is already registered")
        return user_data
    
    user_data = {
        "id": max(CsvUtils.get_csv_values_with_key(users_path, ["id"], main_key="id")) + 1, # Auto increment id
        "login": account_login,
        "password": password,
        "permission_level": 0
    }

    # Add to session cache and save on database
    CsvUtils.save_rows_as_csv(users_path, [user_data], ["id", "login", "password", "permission_level"])
    return user_data

def log_in(account_login: str, password: str, users_path: str) -> dict:
    # Load users
    users = CsvUtils.get_csv_values_with_key(users_path, main_key="login")
    
    user_data = {}

    if not _check_user_exists(account_login, users):
        # Push warning
        return user_data

    if not _check_correct_password(account_login, password, users):
        return user_data
    
    user_data = users[account_login]

    return user_data


def _check_correct_password(account_login: str, password: str, users: dict):
    if users[account_login]["password"] != password:
        # Push warning
        print("WARNING: Wrong password")
        return False
    
    return True

def _check_user_exists(account_login: str, users: dict, push_warning: bool = True):
    if not users.__contains__(account_login):
        # Push warning
        if push_warning:
            print("WARNING: Couldn't find user in database!")
        return False

    return True
