# Armamentos: poderio bélico e tipo de armas, quando for o caso;

class Weapon:
    name: str
    weapon_type: str
    danger_level: float

    def __init__(self, name: str, weapon_type: str, danger_level: float) -> None:
        self.name = name
        self.weapon_type = weapon_type
        self.danger_level = danger_level