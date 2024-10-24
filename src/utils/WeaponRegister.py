import utils.fileUtils.CsvUtils as CsvUtils
from framework.MenuFramework import push_warning, print_colored

# Armamentos: poderio bélico e tipo de armas, quando for o caso;

class Weapon:
    name: str
    weapon_type: str
    danger_level: float

    def __init__(self, name: str, weapon_type: str, danger_level: float) -> None:
        self.name = name
        self.weapon_type = weapon_type
        self.danger_level = danger_level
    
    def get_as_dict(self):
        dictionary = {}
        dictionary["name"] = self.name.lower() # For checking if there is already a weapon with this name
        dictionary["weapon_type"] = self.weapon_type
        dictionary["danger_level"] = self.danger_level

        return dictionary


def register_weapon(weapons_path: str, weapon: Weapon):
    registered_weapons = CsvUtils.get_csv_values_with_key(weapons_path, ["id", "name"], "id")
    weapon_dict = weapon.get_as_dict()
    id = 0
    if len(registered_weapons) > 0:
        id = max(registered_weapons) + 1
    weapon_dict["id"] = id

    if _check_weapon_already_exists(weapons_path, weapon_dict["name"]):
        return

    CsvUtils.save_rows_as_csv(weapons_path, [weapon_dict], ["id", "name", "weapon_type", "danger_level"])
    print_colored("Registered Weapon Sucessfully!", "green")


def get_registered_weapons(weapons_path: str):
    weapons = CsvUtils.get_csv_values_with_key(weapons_path, ["id", "name", "weapon_type", "danger_level"], "id")

    return weapons

def _check_weapon_already_exists(weapons_path: str, weapon_name: str):
    registered_weapons = CsvUtils.get_csv_values_with_key(weapons_path, ["name"], "name")

    if registered_weapons.__contains__(weapon_name):
        # Push Warning:
        push_warning("This weapon was already registered!")
        return True
    
    return False