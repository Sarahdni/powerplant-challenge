import pytest
from src.models import PowerPlant, Fuels
from src.optimizer import ProductionOptimizer

@pytest.fixture
def optimizer():
    return ProductionOptimizer()

@pytest.fixture
def sample_fuels():
    return Fuels(gas=13.4, kerosine=50.8, co2=20, wind=60)

def test_cost_calculation(optimizer, sample_fuels):
    # Test wind turbine (free)
    wind_plant = PowerPlant("wind1", "windturbine", 1.0, 0, 150)
    assert optimizer.calculate_cost_per_mwh(wind_plant, sample_fuels) == 0

    # Test gas plant cost calculation
    gas_plant = PowerPlant("gas1", "gasfired", 0.53, 100, 460)
    expected_cost = (13.4 / 0.53) + (0.3 * 20)
    assert optimizer.calculate_cost_per_mwh(gas_plant, sample_fuels) == expected_cost