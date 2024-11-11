from dataclasses import dataclass
from typing import List

@dataclass
class PowerPlant:
    """
    Represents a power plant with its specifications.

    Attributes:
        name: Identifier of the power plant
        type: Type of plant ('gasfired', 'turbojet', or 'windturbine')
        efficiency: Plant efficiency (0 to 1)
        pmin: Minimum power output in MW
        pmax: Maximum power output in MW
    """
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float

    def validate(self) -> bool:
        """
        Simple validation of powerplant data.

        Returns:
            bool: True if data is valid:
                - Efficiency between 0 and 1
                - Minimum power less than maximum power
                - Valid plant type
        """
        return (
            0 < self.efficiency <= 1 and
            0 <= self.pmin < self.pmax and
            self.type in ["gasfired", "turbojet", "windturbine"]
        )

@dataclass
class Fuels:
    """
    Represents fuel prices and wind conditions.

    Attributes:
        gas: Gas price in euros/MWh
        kerosine: Kerosine price in euros/MWh
        co2: CO2 emission cost in euros/ton
        wind: Wind percentage (0 to 100)
    """
    gas: float
    kerosine: float
    co2: float
    wind: float

    def validate(self) -> bool:
        """
        Simple validation of fuel data.

        Returns:
            bool: True if data is valid:
                - All prices are non-negative
                - Wind percentage between 0 and 100
        """
        return (
            all(price >= 0 for price in [self.gas, self.kerosine, self.co2]) and
            0 <= self.wind <= 100
        )

@dataclass
class PowerPlantOutput:
    """
    Represents the power output for a plant.

    Attributes:
        name: Name of the power plant
        p: Power output in MW
    """
    name: str
    p: float