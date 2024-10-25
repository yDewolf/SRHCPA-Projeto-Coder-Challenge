# Ship registration utils
import utils.fileUtils.CsvUtils as CsvUtils
from framework.MenuFramework import push_warning, print_colored
#from Ship import Ship

class ShipModel:
    model_name: str
    description: str

    material: str
    size: float
    color: str

    weapons: list[int]
    danger: int = -1

    def __init__(self, model_name: str, description: str, size: float, material: str, color: str, weapons: list[int]):
        self.model_name = model_name.lower()
        self.description = description
        self.size = size
        self.material = material
        self.color = color
        self.weapons = weapons

    def get_as_dict(self):
        dictionary = {}
        dictionary["name"] = self.model_name
        dictionary["description"] = self.description
        dictionary["size"] = self.size
        dictionary["material"] = self.material
        dictionary["color"] = self.color
        dictionary["weapons"] = self.weapons
        dictionary["danger"] = self.danger

        return dictionary

class Ship:
    size: float
    material: str

    color: str
    fall_location: str
    weapons: list[int]
    gas: float
    crew: int
    crew_state: str
    damage: int
    danger: int = -1

    model_id: int

    def __init__(self, size: float, material: str, color: str, fall_location: str, gas: float, crew: int, crew_state: str, damage: int, weapons: list[int], model_id: int = -1) -> None:
        self.size = size
        self.material = material
        self.color = color
        self.fall_location = fall_location
        self.gas = gas
        self.crew = crew
        self.crew_state = crew_state
        self.weapons = weapons
        self.damage = damage
        self.model_id = model_id


    def get_size_as_str(self):
        if self.size > 1 and self.size <= 5:
            return "Pequena"
        
        if self.size > 5 and self.size <= 10:
            return "Média"
        
        if self.size > 10 and self.size <= 20:
            return "Grande"
        
        if self.size > 20 and self.size <= 50:
            return "Gigante"
        
        if self.size > 50 and self.size <= 100:
            return "Colossal"
    
    def get_damage_as_str(self):
        if self.damage == 0:
            return "Sem avarias"
        
        if self.damage == 1:
            return "Praticamene Intacta"
        
        if self.damage == 2:
            return "Parcialmente Destruída"
        
        if self.damage == 3:
            return "Muito Destruida"
        
        if self.damage == 4:
            return "Perda Total"
        
    
    def get_as_dict(self):
        dictionary = {}
        dictionary["size"] = self.size
        dictionary["material"] = self.material     
        dictionary["color"] = self.color
        dictionary["fall_location"] = self.fall_location
        dictionary["gas"] = self.gas
        dictionary["crew"] = self.crew
        dictionary["crew_state"] = self.crew_state
        dictionary["damage"] = self.damage
        dictionary["weapons"] = self.weapons
        dictionary["danger"] = self.danger
        
        return dictionary


def ship_from_ship_model(models_path: str, model_id: int, fall_location: str, gas: float, damage: int, crew: int, crew_state: str):
    ship_model = CsvUtils.get_csv_values_with_key(models_path, ["id", "name", "size", "material", "color", "weapons"], "id")[model_id]
    
    ship = Ship(
        ship_model["size"],
        ship_model["material"],
        ship_model["color"],
        fall_location,
        gas,
        crew,
        crew_state,
        damage,
        ship_model["weapons"],
        model_id
    )

    return ship


def register_ship(ships_path: str, ship: Ship):
    # Save on database
    ship_dict = ship.get_as_dict()
    registered_ids = CsvUtils.get_csv_values_with_key(ships_path, ["id"], "id")
    id = 0
    if len(registered_ids) > 0:
        id = max(registered_ids) + 1
    
    ship_dict["id"] = id

    CsvUtils.save_rows_as_csv(ships_path, [ship_dict])
    print_colored("Registered Ship Sucessfully!", "green")


def register_ship_model(ship_models_path: str, ship_model: ShipModel):
    model_dict = ship_model.get_as_dict()
    model_dict["name"] = model_dict["name"]
    model_dict["danger"] = -1
    if _check_model_exists(ship_models_path, model_dict["name"]):
        return

    registered_ids = CsvUtils.get_csv_values_with_key(ship_models_path, ["id"], "id")
    id = 0
    if len(registered_ids) > 0:
        id = max(registered_ids) + 1
    
    model_dict["id"] = id
    CsvUtils.save_rows_as_csv(ship_models_path, [model_dict])
    print_colored("Registered Model Sucessfully!", "green")


def _check_model_exists(ship_models_path: str, model_name: str):
    ship_models = CsvUtils.get_csv_values_with_key(ship_models_path, ["name"], "name")
    if ship_models.__contains__(model_name):
        # Push Warning:
        push_warning("This ship model already exists!")
        return True
    
    return False

def get_registered_models(ship_models_path: str):
    #Header: id,name,description,size,color,weapons,danger
    registered_models = CsvUtils.get_csv_values_with_key(ship_models_path, ["id", "name", "description", "size", "color", "weapons"], "id")

    return registered_models