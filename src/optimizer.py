from typing import List, Tuple
from src.models import PowerPlant, Fuels, PowerPlantOutput

class ProductionOptimizer:
    def calculate_cost_per_mwh(self, plant: PowerPlant, fuels: Fuels) -> float:
        """
        Calculate the cost per MWh for each plant type.
        """
        if plant.type == "windturbine":
            return 0
        elif plant.type == "gasfired":
            fuel_cost = fuels.gas / plant.efficiency
            co2_cost = (0.3 * fuels.co2)  # CO2 cost per MWh
            return fuel_cost + co2_cost
        elif plant.type == "turbojet":
            return fuels.kerosine / plant.efficiency
        else:
            raise ValueError(f"Unknown plant type: {plant.type}")

    def get_actual_capacity(self, plant: PowerPlant, fuels: Fuels) -> Tuple[float, float]:
        """
        Get actual min/max capacity considering wind percentage for windturbines.
        """
        if plant.type == "windturbine":
            max_power = plant.pmax * (fuels.wind / 100.0)
            return (0, max_power)
        else:
            return (plant.pmin, plant.pmax)

def calculate_production_plan(
    load: float,
    fuels: Fuels,
    power_plants: List[PowerPlant]
) -> List[PowerPlantOutput]:
    """
    Initial version: just allocate minimum power to each plant.
    """
    optimizer = ProductionOptimizer()
    result = []
    
    for plant in power_plants:
        min_power, max_power = optimizer.get_actual_capacity(plant, fuels)
        result.append(PowerPlantOutput(name=plant.name, p=min_power))
    
    return result