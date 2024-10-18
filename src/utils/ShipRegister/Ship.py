# Ship class with its variables and functions

# Tamanho: pequena, média, grande ou colossal;
# Cor: vermelha, laranja, amarela, verde, azul, anil ou violeta;
# Local de queda: continente ou oceano onde a nave caiu;
# Armamentos: poderio bélico e tipo de armas, quando for o caso;
# Tipo de combustível: use a imaginação!
# Número de tripulantes e estado dos tripulantes: Quantos sobreviveram e como estão?
# Grau de avaria, variando entre: “perda total”, “muito destruída”, “parcialmente destruída”, “praticamente intacta” e “sem avarias”;
# Potencial de prospecção tecnológica: avalia o valor científico e tecnológico que uma nave alienígena pode oferecer;
# Grau de periculosidade: determina o risco envolvido em se aproximar e interagir com a nave;

class Ship:
    size: float
    color: str
    fall_location: str
    weapons: list
    gas: str
    crew: int
    crew_state: str
    damage: int
    danger: int

    def __init__(self, size: float, color: str, fall_location: str, gas: str, crew: int, crew_state: str, damage: int) -> None:
        self.size = size
        self.color = color
        self.fall_location = fall_location
        self.gas = gas
        self.crew = crew
        self.crew_state = crew_state
        self.damage = damage 


    def get_size(self):
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
        
    def damage_aplied(self):
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
        
        
        
        
