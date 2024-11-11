import pytest
from models import PowerPlant, Fuels

def test_powerplant_validation():
    """Verify powerplant validation works for both valid and invalid inputs"""
    # Test valid plant
    valid_plant = PowerPlant("gas1", "gasfired", 0.53, 100, 460)
    assert valid_plant.validate() is True

    # Test invalid plant
    invalid_plant = PowerPlant("gas1", "gasfired", 1.5, 100, 460)
    assert invalid_plant.validate() is False


def test_fuels_validation_errors():
    """Test various invalid fuels configurations"""
    invalid_fuels = [
        Fuels(gas=-1, kerosine=50.8, co2=20, wind=60),     # negative gas
        Fuels(gas=13.4, kerosine=-1, co2=20, wind=60),     # negative kerosine
        Fuels(gas=13.4, kerosine=50.8, co2=-1, wind=60),   # negative co2
        Fuels(gas=13.4, kerosine=50.8, co2=20, wind=-10),  # wind < 0
        Fuels(gas=13.4, kerosine=50.8, co2=20, wind=150)   # wind > 100
    ]
    for fuels in invalid_fuels:
        assert fuels.validate() is False