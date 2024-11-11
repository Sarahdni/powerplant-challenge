class PowerPlant:
    def __init__(self, name: str, type: str, efficiency: float, pmin: float, pmax: float):
        self.name = name
        self.type = type
        self.efficiency = efficiency
        self.pmin = pmin
        self.pmax = pmax

class Fuels:
    def __init__(self, gas: float, kerosine: float, co2: float, wind: float):
        self.gas = gas
        self.kerosine = kerosine
        self.co2 = co2
        self.wind = wind