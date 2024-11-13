from typing import List, Dict, Tuple
import logging
from models import PowerPlant, Fuels, PowerPlantOutput  # Enlève 'src.'

logger = logging.getLogger(__name__)

class ProductionOptimizer:
    def calculate_cost_per_mwh(self, plant: PowerPlant, fuels: Fuels) -> float:
        if plant.type == "windturbine":
            return 0
        elif plant.type == "gasfired":
            fuel_cost = fuels.gas / plant.efficiency
            co2_cost = (0.3 * fuels.co2)  
            return fuel_cost + co2_cost
        elif plant.type == "turbojet":
            return fuels.kerosine / plant.efficiency
        else:
            raise ValueError(f"Unknown plant type: {plant.type}")

    def get_actual_capacity(self, plant: PowerPlant, fuels: Fuels) -> Tuple[float, float]:
        if plant.type == "windturbine":
            max_power = plant.pmax * (fuels.wind / 100.0)
            return (0, max_power)
        else:
            return (plant.pmin, plant.pmax)

    
    def optimize(self, load: float, fuels: Fuels, plants: List[PowerPlant]) -> List[PowerPlantOutput]:
        # Initialize allocations dictionary
        allocations = {p.name: 0.0 for p in plants}
        """
        Optimize the power production plan using a recursive backtracking approach.
        
        Args:
            load: Required power load in MW
            fuels: Current fuel prices and wind percentage
            plants: Available power plants
            
        Returns:
            List of power allocations for each plant
            
        Raises:
            ValueError: If load requirement cannot be met
        """
        
        # 1. Prepare plant information
        plant_infos = []
        for plant in plants:
            min_power, max_power = self.get_actual_capacity(plant, fuels)
            cost = self.calculate_cost_per_mwh(plant, fuels)
            if max_power > 0:  # Ne considérer que les centrales disponibles
                plant_infos.append({
                    'plant': plant,
                    'min_power': min_power,
                    'max_power': max_power,
                    'cost': cost,
                    'efficiency': plant.efficiency
                })
        
        # 2. Sort plants by cost and efficiency
        # Lower cost and higher efficiency are prioritized
        plant_infos.sort(key=lambda x: (x['cost'], -x['efficiency']))
        
        def try_allocate(remaining_load, available_plants, current_allocations):
            if abs(remaining_load) < 0.1:  # Solution found
                return current_allocations
            if remaining_load < 0 or not available_plants:  # No solution
                return None
                
            plant_info = available_plants[0]
            rest_plants = available_plants[1:]
            
            # Try different possible power allocations for current plant
            possible_powers = []
            min_p = plant_info['min_power']
            max_p = plant_info['max_power']
            
            if min_p <= remaining_load:
                possible_powers.append(min(max_p, remaining_load))
                if min_p < remaining_load:
                    possible_powers.append(min_p)
            
            # Try each possible power allocation
            for power in possible_powers:
                new_allocations = current_allocations.copy()
                new_allocations[plant_info['plant'].name] = power
                result = try_allocate(remaining_load - power, rest_plants, new_allocations)
                if result is not None:
                    return result
                    
            return try_allocate(remaining_load, rest_plants, current_allocations)
        
        # 3. Find optimal allocation
        final_allocations = try_allocate(load, plant_infos, allocations)
        
        if final_allocations is None:
            raise ValueError(f"Cannot meet load requirement. Required: {load}MW")
        
        # 4. Create result in correct order
        result = []
        # Wind turbines first
        for plant in plants:
            if plant.type == "windturbine":
                result.append(PowerPlantOutput(
                    name=plant.name,
                    p=round(final_allocations[plant.name], 1)
                ))
        # Then other plants
        for plant in plants:
            if plant.type != "windturbine":
                result.append(PowerPlantOutput(
                    name=plant.name,
                    p=round(final_allocations[plant.name], 1)
                ))

        # 5. Final validation
        total_production = sum(p.p for p in result)
        if abs(total_production - load) > 0.1:
            raise ValueError(
                f"Cannot meet load requirement. Required: {load}MW, Produced: {total_production}MW"
            )
        
        return result
    
        
        

def calculate_production_plan(
    load: float,
    fuels: Fuels,
    power_plants: List[PowerPlant]
) -> List[PowerPlantOutput]:
    optimizer = ProductionOptimizer()
    return optimizer.optimize(load, fuels, power_plants)