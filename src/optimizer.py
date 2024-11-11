from typing import List, Dict, Tuple
import logging
from src.models import PowerPlant, Fuels, PowerPlantOutput

logger = logging.getLogger(__name__)

class ProductionOptimizer:
    def calculate_cost_per_mwh(self, plant: PowerPlant, fuels: Fuels) -> float:
        """Calculate the cost per MWh for each plant type."""
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
        """Get actual min/max capacity considering wind percentage for windturbines."""
        if plant.type == "windturbine":
            max_power = plant.pmax * (fuels.wind / 100.0)
            return (0, max_power)
        else:
            return (plant.pmin, plant.pmax)

    def optimize(self, load: float, fuels: Fuels, plants: List[PowerPlant]) -> List[PowerPlantOutput]:
        """
        Optimize the power production plan based on load demand and current conditions.
        """
        # 1/ Initialize power allocations
        wind_plants = [p for p in plants if p.type == "windturbine"]
        gas_plants = [p for p in plants if p.type == "gasfired"]
        other_plants = [p for p in plants if p not in wind_plants + gas_plants]
        allocations = {p.name: 0.0 for p in plants}
        remaining_load = load

        # 2. Allocate wind plants first (zero cost)
        for plant in wind_plants:
            _, max_power = self.get_actual_capacity(plant, fuels)
            power = min(max_power, remaining_load)
            allocations[plant.name] = power
            remaining_load -= power

        # 3. Sort gas plants by efficiency
        efficient_plants = [p for p in gas_plants if p.efficiency > 0.5]
        less_efficient_plants = [p for p in gas_plants if p.efficiency <= 0.5]

        # 4. Allocation strategy based on remaining load
        if remaining_load > 0:
            # 4a. Allocate minimum loads to efficient plants if possible
            for plant in efficient_plants:
                if remaining_load >= plant.pmin:
                    allocations[plant.name] = plant.pmin
                    remaining_load -= plant.pmin

            # 4b. Distribute remaining load to efficient plants
            for plant in efficient_plants:
                additional_power = min(
                    plant.pmax - allocations[plant.name],
                    remaining_load
                )
                allocations[plant.name] += additional_power
                remaining_load -= additional_power

            # 4c. Use less efficient plants if needed
            if remaining_load > 0:
                for plant in less_efficient_plants:
                    if remaining_load >= plant.pmin:
                        power = min(plant.pmax, remaining_load)
                        allocations[plant.name] = power
                        remaining_load -= power

        # 5. Create result in correct order
        result = []
        for plant in plants:  
            result.append(PowerPlantOutput(
                name=plant.name,
                p=round(allocations[plant.name], 1)
            ))

        # 6. Validate total production matches load
        total_production = sum(p.p for p in result)
        if abs(total_production - load) > 0.1:
            raise ValueError(
                f"Cannot meet load requirement. "
                f"Required: {load}MW, "
                f"Produced: {total_production}MW"
            )

        return result

def calculate_production_plan(
    load: float,
    fuels: Fuels,
    power_plants: List[PowerPlant]
) -> List[PowerPlantOutput]:
    """Calculate the optimal production plan."""
    optimizer = ProductionOptimizer()
    return optimizer.optimize(load, fuels, power_plants)