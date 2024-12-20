# Main implementation
from utils.Session.Session import Session
from framework.MenuFramework import MenuHandler, Menu, MenuOption, bool_input_value, range_input_value, list_input_value, push_warning, print_colored
from utils.fileUtils.CsvUtils import get_formatted_csv
import utils.Session.SessionUtils as SessionUtils
import utils.WeaponRegister as WeaponryRegister
import utils.ShipRegister as ShipRegister
import utils.KeyUtils as KeyUtils

from utils.ShipRegister import Ship
from utils.ShipClassifier import classify_ship, calculate_ship_danger


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
    print_colored("Signed out from account successfully!", "green")

def login_account_option():
    try_again: bool = True
    while try_again:
        login = input("Insert an account login: ")
        password = input("Type the password: ")

        user_data = SessionUtils.log_in(login, password, current_session.cache["users_path"])
        if user_data != {}:
            current_session.log_in(user_data)
            print_colored("Logged into account successfully!", "green")
            try_again = False
            break
        
        # Push warning:
        push_warning("Invalid User or Incorrect password!")
        if not bool_input_value("Do you want to try again?"):
            break

def create_account_option():
    try_again: bool = True
    while try_again:
        login = input("Insert an account login: ")
        password = input("Type the password: ")

        # Forma óbviamente segura de se certificar que alguém tem uma chave de certificação
        # Com certeza ninguém conseguiria modificar o valor de perm level 
        # e criar uma conta com permissões que ela não devia ter
        perm_level = 0
        if bool_input_value("Do you have a certification key? "):
            try_key_again = True
            while try_key_again:
                key = input("Insert your certification key: ")

                perm_level = KeyUtils.check_registered_key(key, current_session.cache["keys_path"])
                if perm_level > 0:
                    break

                if not bool_input_value("Do you want to try again? "):
                    try_key_again = False
                    break

        user_data = SessionUtils.create_account(login, password, perm_level, current_session.cache["users_path"])
        if user_data != {}:
            current_session.log_in(user_data)
            print_colored("Created account successfully!", "green")
            try_again = False
            break
        
        if not bool_input_value("Do you want to try again? "):
            break


def show_users_database():
    print(get_formatted_csv(current_session.cache["users_path"], ["id", "login", "permission_level"]))

def show_weaponry_database():
    print(get_formatted_csv(current_session.cache["weaponry_path"], ["id", "name", "weapon_type", "danger_level"]))

def show_ship_models_database():
    print(get_formatted_csv(current_session.cache["ship_models_path"], ["id", "name", "description", "size", "color", "weapons"]))


def register_weaponry():
    #id,name,weapon_type,danger_level
    name = ""
    weapon_type = ""
    danger_level = 0

    confirm = False
    while not confirm:
        name = input("Type the name of the weapon: ")
        if WeaponryRegister._check_weapon_already_exists(current_session.cache["weaponry_path"], name):
            continue

        weapon_type = input("What type of weapon it is? ")
        danger_level = range_input_value(0, 10, "In a range of 0 to 10, 0 being no danger and 10 being extinction level of danger, how you classify this weapon? ")
        
        confirm = bool_input_value(f"Are you sure about those informations? \nWeapon Name: {name}\nWeapon Type: {weapon_type}\nDanger Level: {danger_level}\n")
    
    weapon = WeaponryRegister.Weapon(name, weapon_type, danger_level)
    WeaponryRegister.register_weapon(current_session.cache["weaponry_path"], weapon)

def register_ship_model():
    #id, name, description, size, color, weapons
    name: str = ""
    size: float = -1
    material: str = ""
    color: str = ""
    weapons: list[int] = []

    confirm = False
    while not confirm:
        name = input("Type the name of the ship model: ")
        if ShipRegister._check_model_exists(current_session.cache["ship_models_path"], name):
            continue
        
        color = input("Color of the ship model: ")
        size = input("Size of the ship model (in Meters): ")
        material = input("What material the ship model is (mostly) made of? ")
        weapons = _select_weapons()
        
        description = input("Give this ship model a brief description: ")
        
        confirm = bool_input_value(f"Are you sure about the following informations? \nModel Name: {name}\nModel Description: {description}\nShip size: {size}\nMaterial: {material}\nShip color: {color}\nWeapon ids: {weapons}\n")
    
    ship_model = ShipRegister.ShipModel(name, description, size, material, color, weapons)
    ship = Ship(size, material, color, "", -1, 0, "", 0, weapons)
    ship_model.danger = calculate_ship_danger(ship, current_session.cache)

    ShipRegister.register_ship_model(current_session.cache["ship_models_path"], ship_model)
    

def register_ship():
    #id, size, color, fall_location, weapons, gas, crew, crew_state, damage, danger

    size: float = -1
    color: str = ""
    material: str = ""
    weapons: list[int] = []

    confirm = False
    while not confirm:
        color = input("Color of the ship: ")
        size = range_input_value(0, 65536,"Size of the ship (in Meters): ")
        material = input("What material the ship was (mostly) made of? ")
        
        weapons = _select_weapons()

        confirm = bool_input_value(f"Are you sure about the following informations?\nShip size: {size}\nMaterial: {material}\nShip color: {color}\nWeapon ids: {weapons}\n")
    
    ship_info = _input_ship_info()

    ship = ShipRegister.Ship(size, 
                             material,
                             color,
                             ship_info["fall_location"], 
                             ship_info["gas"], 
                             ship_info["crew"],
                             ship_info["crew_state"],
                             ship_info["damage"],
                             weapons)
    ship.danger = calculate_ship_danger(ship, current_session.cache)

    ShipRegister.register_ship(current_session.cache["ships_path"], ship)

def register_ship_with_preset():
    #id, size, color, fall_location, weapons, gas, crew, crew_state, damage, danger
    selected_model_id = -1

    # Model selection
    confirm_model = False
    while not confirm_model:
        registered_models = ShipRegister.get_registered_models(current_session.cache["ship_models_path"])
        available_models = []
        for weapon_id in registered_models:
            available_models.append(weapon_id)
            model_dict = registered_models[weapon_id]

            print(f"[{weapon_id}]-{model_dict["name"]}\nDescription: {model_dict["description"]}\nSize: {model_dict["size"]}\nColor: {model_dict["color"]}\n")
        
        selected_model_id = list_input_value(available_models, "Select a ship model by typing its number: ")

        confirm_model = bool_input_value(f"Confirm this model? (Id: {selected_model_id}): ")
    
    ship_info = _input_ship_info()

    ship = ShipRegister.ship_from_ship_model(current_session.cache["ship_models_path"], selected_model_id,
                                            ship_info["fall_location"],
                                            ship_info["gas"],
                                            ship_info["damage"],
                                            ship_info["crew"],
                                            ship_info["crew_state"])
    ship.danger = calculate_ship_danger(ship, current_session.cache)

    ShipRegister.register_ship(current_session.cache["ships_path"], ship)


def _select_weapons():
    weapons = []

    confirm_weapons = False
    while not confirm_weapons:
        available_weapons = [-1]
        registered_weapons = WeaponryRegister.get_registered_weapons(current_session.cache["weaponry_path"])
        print("\nRegistered Weapons:")
        for weapon_id in registered_weapons:
            available_weapons.append(weapon_id)
            print(f"[{weapon_id}]-{registered_weapons[weapon_id]["name"]}")
        
        selected_weapon_id = list_input_value(available_weapons, "Select a weapon by typing its number (Type -1 if there are no weapons): ", -2)
        weapons.append(selected_weapon_id)

        confirm_weapons = bool_input_value(f"Have you finished adding weapons?\nSelected weapons: {weapons}\n")
    
    return weapons

def _input_ship_info():
    fall_location: str = ""
    gas: float = -1
    damage: float = -1
    crew_state: str = ""
    crew: int = -1

    ship_info = {}

    confirm = False
    while not confirm:
        fall_location = input("The ship landed on: ")
        gas = float(input("How much gas (in Kilo Liters) there was in the ship (type -1 if you don't know): "))
        damage = range_input_value(0, 100, "In a scale of 0 to 100, how damaged was the ship? ")
        crew = range_input_value(0, 65536, "How much crew was in the ship? ")
        crew_state = input("What state the crew was? ")

        confirm = bool_input_value(f"Do you confirm the following information?\nShip fall location: {fall_location}\nGas: {gas}\nDamage: {damage}\nCrew: {crew}\nCrew state: {crew_state}")

    ship_info["fall_location"] = fall_location
    ship_info["gas"] = gas
    ship_info["damage"] = damage
    ship_info["crew_state"] = crew_state
    ship_info["crew"] = crew

    return ship_info

# Menu options

register_weaponry_option = MenuOption(register_weaponry, "Register a Weapon", view_database_permission_level)

ship_model_register_option = MenuOption(register_ship_model, "Register a Ship model", view_database_permission_level)
ship_register_option = MenuOption(register_ship, "Register a Ship")
ship_register_with_preset = MenuOption(register_ship_with_preset, "Register a Ship based on a model")


login_account = MenuOption(login_account_option, "Log in an Account", is_logged, inverse_condition=True)
signout_account = MenuOption(signout_account_option, "Sign out", is_logged)
create_account = MenuOption(create_account_option, "Create an Account")

# Menu implementation


weaponry_register_menu = Menu(4, "Weaponry Menu", [
    register_weaponry_option
    #MenuOption(show_weaponry_database, "Show Weaponry Database")
])

ship_register_menu = Menu(3, "Register Ships Menu", [ship_register_with_preset, ship_register_option, ship_model_register_option])

database_menu = Menu(2, "Database Menu", [
    MenuOption(show_users_database, "Show Users Database"),
    MenuOption(show_ship_models_database, "Show Ship Models database"),
    MenuOption(show_weaponry_database, "Show weaponry database")
    ])

account_menu = Menu(1, "Account menu", [create_account, signout_account, login_account])

main_menu = Menu(0, "Main Menu", [
    MenuOption(account_menu),
    MenuOption(ship_register_menu, visibility_condition=is_logged),
    MenuOption(database_menu, visibility_condition=view_database_permission_level),
    MenuOption(weaponry_register_menu, visibility_condition=view_database_permission_level)
])
main_menu.exit_option_text = "Quit"


menu_handler = MenuHandler(main_menu)

# Very simple way of showing the cool title

print('  ___________________  ___ ___  ___________________  _____   ')
print(' /   _____/\______   \/   |   \ \_   ___ \______   \/  _  \  ')
print(' \_____  \  |       _/    ~    \/    \  \/|     ___/  /_\  \ ')
print(' /        \ |    |   \    Y    /\     \___|    |  /    |    \ ')
print('/_______  / |____|_  /\___|_  /  \______  /____|  \____|__  /')
print('        \/         \/       \/          \/                \/ ')

print_colored("\nWelcome to SRHCPA (Sistema de Recuperação Humana Contra Patos Alienígenas)\n", "cyan")
print("Our objective is to register every ship from Alien Ducks and from us Humans")
print("For that we will need your help to register every ship you find!")

menu_handler.main_loop()