# Main implementation
from utils.Session.Session import Session
from framework.MenuFramework import MenuHandler, Menu, MenuOption, bool_input_value
from utils.fileUtils.CsvUtils import get_formatted_csv
import utils.Session.SessionUtils as SessionUtils

current_session = Session()


# Menu conditions

def is_logged(menu_handler: MenuHandler):
    menu_handler.global_variables["SessionLogged"] = current_session
    return current_session.logged_in

def view_database_permission_level(menu_handler: MenuHandler):
    if not is_logged(menu_handler):
        return False
    
    if current_session.user_data["permission_level"] > 2:
        return True
    
    return False

# Option functions

def signout_account_option():
    current_session.sign_out()

def login_account_option():
    try_again: bool = True
    while try_again:
        login = input("Insert an account login: ")
        password = input("Type the password: ")

        user_data = SessionUtils.log_in(login, password, current_session.cache["users_path"])
        if user_data != {}:
            current_session.log_in(user_data)
            try_again = False
            break
        
        # Push warning:
        print("WARNING: Invalid User or Incorrect password!")
        if not bool_input_value("Do you want to try again?"):
            break

def create_account_option():
    try_again: bool = True
    while try_again:
        login = input("Insert an account login: ")
        password = input("Type the password: ")

        user_data = SessionUtils.create_account(login, password, current_session.cache["users_path"])
        if user_data != {}:
            current_session.log_in(user_data)
            try_again = False
            break
        
        # Push warning:
        if not bool_input_value("Do you want to try again? "):
            break


def show_users_database():
    print(get_formatted_csv(current_session.cache["users_path"], ["id", "login", "permission_level"]))

# Menu options


login_account = MenuOption(login_account_option, "Log in an Account", is_logged, inverse_condition=True)
signout_account = MenuOption(signout_account_option, "Sign out", is_logged)
create_account = MenuOption(create_account_option, "Create an Account")

show_users_database = MenuOption(show_users_database, "Show Users Database")

# Menu implementation

database_menu = Menu(2, "Database Menu", [show_users_database])

account_menu = Menu(1, "Account menu", [create_account, signout_account, login_account])

main_menu = Menu(0, "Main Menu", [MenuOption(account_menu), MenuOption(database_menu, visibility_condition=view_database_permission_level)])

menu_handler = MenuHandler(main_menu)
menu_handler.main_loop()