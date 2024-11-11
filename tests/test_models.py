import pytest
from src.models import PowerPlant, Fuels

def test_powerplant_validation():
    """Verify powerplant validation works for both valid and invalid inputs"""
    # Test valid plant
    valid_plant = PowerPlant("gas1", "gasfired", 0.53, 100, 460)
    assert valid_plant.validate() is True

    # Test invalid plant
    invalid_plant = PowerPlant("gas1", "gasfired", 1.5, 100, 460)
    assert invalid_plant.validate() is False

def test_fuels_validation():
    """Test fuel validation"""
    invalid_fuels = Fuels(gas=-1, kerosine=50.8, co2=20, wind=60)
    assert invalid_fuels.validate() is False