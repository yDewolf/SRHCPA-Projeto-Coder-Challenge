from utils.ShipRegister import Ship
from utils.WeaponRegister import get_weapon_objects, Weapon

# Ship classification algorithm

# Poderia simplesmente criar outra tabela com as chaves e os seus respectivos valores
# porém é mais fácil só deixar esses dicionários aqui mesmo...

# Material : General value per m²
registered_materials: dict = {
    "plasteel": 5000,
    "carbon fiber": 2500,
    "stainless steel": 1000,
    "inconel": 800,
    "aluminium": 500.5
}
registered_weapon_types: dict = {
    "ballistic": 300.0,
    "explosive": 600.25,
    "lazer": 7270.5
}

damage_discount_multiplier: float = 2
damaged_weapon_discount_multiplier: float = 2
general_gas_value: float = 7500

ship_size_ratio: float = 250



def classify_ship(ship: Ship, session_cache: dict):
    damage_discount = _calculate_damage_discount(ship)

    ship_danger = calculate_ship_danger(ship, session_cache, damage_discount)
    ship_value = calculate_ship_value(ship, session_cache, damage_discount)

    danger_as_str = ""
    if ship_danger <= 1:
        danger_as_str = "Not dangerous at all"
    elif ship_danger <= 3:
        danger_as_str = "Not very dangerous"
    elif ship_danger <= 6:
        danger_as_str = "Dangerous"
    elif ship_danger <= 9:
        danger_as_str = "Very Dangerous"
    elif ship_danger <= 15:
        danger_as_str = "Catastrophical"
    else:
        danger_as_str = "Can extinct us"
    
    value_as_str = ""

    if ship_value <= 7500:
        value_as_str = "Barely useful"
    elif ship_value <= 75000:
        value_as_str = "Space Scraps"
    elif ship_value <= 150000:
        value_as_str = "Kinda valuable"
    elif ship_value <= 300000:
        value_as_str = "Valuable"
    elif ship_value <= 750000:
        value_as_str = "Very valuable"
    elif ship_value <= 1300000:
        value_as_str = "Really valuable"
    else:
        value_as_str = "Elite Ship"
    
    ship_classification = {
        "danger_level": ship_danger,
        "value": ship_value,
        "danger": danger_as_str,
        "valuability": value_as_str
    }

    return ship_classification


# Gráfico no Desmos
# https://www.desmos.com/calculator/is66pnsmux?lang=pt-BR

# Os principais fatores que agregam valor a uma nave é seu tamanho, material e o quão danificada ela foi
# 1º Calculamos o desconto do dano, esse valor é usado para diminuir valores do:
# - Material
# - Armamento
#
# 2º Calculamos o valor total do material multiplicando o tamanho da nave por valor do material / desconto do dano
# Dessa forma quando o desconto de dano for maior, o valor de material será diminuído
#  
# 3º Calculamos o preço do combústivel, este é bem simples é só multiplicar o tanto de combústivel pelo valor geral de combústivel
#
# 4º Caculamos o preço do armamento que é:
# nível de perigo * o valor do tipo de armamento / desconto de dano * multiplicador de desconto de dano para armas
#
# Este multiplicador de desconto serve para controlar melhor como o desconto de dano é aplicado em armamentos,
# neste caso ele é maior do que 1, o que significa que armas danificadas são menos valorizadas do que materiais por exemplo.

def calculate_ship_value(ship: Ship, session_cache: dict, damage_discount: float = -1):
    ship_value: float = 0
    # The more damaged the ship less value its materials will represent
    # Material multiplier = Ship material value multiplier * (Ship damage in percentage * damage_discount_multiplier)

    if damage_discount <= 0:
        damage_discount = _calculate_damage_discount(ship)

    # Ship damage + 1 since you can't divide by 0
    material_value = registered_materials.get(ship.material.lower(), 100)
    total_material_value = ship.size * (material_value / damage_discount)

    # Gas is measured in Kilo Liters
    # Most of the ships use Liquid Hydrogen or Liquid Oxygen

    # Gas multiplier = Gas in ship * general value
    gas_value = ship.gas * general_gas_value

    # Ship.gas can be -1 since you can input -1 if you don't know if the ship has fuel or not
    if gas_value < 0: gas_value = 1

    registered_weapons: list[Weapon] = get_weapon_objects(session_cache["weaponry_path"])

    total_weaponry_value: float = 0.0
    # This could be pre calculated and added as a column in weaponry table
    for weapon_id in ship.weapons:
        if not registered_weapons.__contains__(weapon_id):
            continue
        
        weapon_dict = registered_weapons[weapon_id]
        # Weapon danger level * Weapon type value
        weapon_value = weapon_dict["danger_level"] * (registered_weapon_types.get(weapon_dict["weapon_type"].lower(), 1)) / (damage_discount * damaged_weapon_discount_multiplier)
        total_weaponry_value += weapon_value

    ship_value = total_material_value + gas_value + total_weaponry_value
    print(f"Material Value: {total_material_value}\nGas Value: {gas_value}\nWeaponry value: {total_weaponry_value}\nDamage Discount: {damage_discount}")

    return ship_value

def calculate_ship_danger(ship: Ship, session_cache: dict, damage_discount: float = -1):
    ship_danger_score = 0.0

    if damage_discount <= 0:
        damage_discount = _calculate_damage_discount(ship)

    gas = ship.gas

    if gas < 0:
        gas = 0

    general_danger_score = ship.size + gas

    registered_weapons: list[Weapon] = get_weapon_objects(session_cache["weaponry_path"])

    total_weaponry_danger: float = 0.0
    # This could be pre calculated and added as a column in weaponry table
    for weapon_id in ship.weapons:
        if not registered_weapons.__contains__(weapon_id):
            continue
        
        weapon_dict = registered_weapons[weapon_id]

        weapon_danger = weapon_dict["danger_level"]

        total_weaponry_danger += weapon_danger


    potential_danger = general_danger_score + total_weaponry_danger

    # Kinda of a normalization method
    # Multiplies by ship size so bigger ships are more dangerous
    ship_danger_score = ((potential_danger / damage_discount) / potential_danger) * ship.size / ship_size_ratio

    return int(ship_danger_score)

def _calculate_damage_discount(ship: Ship):
    damage_discount = ((int(ship.damage) + 1) / 100 * damage_discount_multiplier)
    damage_discount = damage_discount ** 0.75

    return damage_discount
    