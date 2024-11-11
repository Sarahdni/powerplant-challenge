import pytest
import json
import os
from src.models import PowerPlant, Fuels
from src.optimizer import ProductionOptimizer

@pytest.fixture
def payload1_data():
    """Load test data from payload1.json"""
    file_path = os.path.join(os.path.dirname(__file__), '..', 'payloads', 'payload1.json')
    with open(file_path, 'r') as f:
        return json.load(f)

def test_payload1_scenario(payload1_data):
    """Test standard load scenario with 60% wind"""
    optimizer = ProductionOptimizer()
    
    # Create test objects
    fuels = Fuels(
        gas=payload1_data['fuels']['gas(euro/MWh)'],
        kerosine=payload1_data['fuels']['kerosine(euro/MWh)'],
        co2=payload1_data['fuels']['co2(euro/ton)'],
        wind=payload1_data['fuels']['wind(%)']
    )
    
    powerplants = [
        PowerPlant(
            name=p['name'],
            type=p['type'],
            efficiency=p['efficiency'],
            pmin=p['pmin'],
            pmax=p['pmax']
        )
        for p in payload1_data['powerplants']
    ]

    # Test optimization
    result = optimizer.optimize(payload1_data['load'], fuels, powerplants)
    
    # Verify total matches load
    total_power = sum(plant.p for plant in result)
    assert abs(total_power - payload1_data['load']) < 0.1
    
    # Verify wind plants are prioritized
    wind_plants = [p for p in result if any(pp.type == "windturbine" 
                                            for pp in powerplants if pp.name == p.name)]
    assert all(p.p > 0 for p in wind_plants)




