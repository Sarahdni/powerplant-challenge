from dataclasses import dataclass
from typing import List

@dataclass
class PowerPlant:
    """
    Represents a power plant with its specifications.
    """
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float

    def validate(self) -> bool:
        """
        Simple validation of powerplant data.
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
    """
    gas: float
    kerosine: float
    co2: float
    wind: float

    def validate(self) -> bool:
        """
        Simple validation of fuel data.
        """
        return (
            all(price >= 0 for price in [self.gas, self.kerosine, self.co2]) and
            0 <= self.wind <= 100
        )