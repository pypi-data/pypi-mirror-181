"""
general concepts
"""

from enum import Enum, auto
from typing import Dict, Set


class Fuel(Enum):
    HYDRO = auto()
    WIND = auto()
    OTHER_RENEWABLES = auto()
    NUCLEAR = auto()
    NATURAL_GAS = auto()
    DUAL_FUEL = auto()
    OTHER_FOSSIL_FUELS = auto()


NAME: Dict[Fuel, str] = {
    Fuel.HYDRO: "Hydro",
    Fuel.WIND: "Wind",
    Fuel.OTHER_RENEWABLES: "Other Renewables",
    Fuel.NUCLEAR: "Nuclear",
    Fuel.NATURAL_GAS: "Natural Gas",
    Fuel.DUAL_FUEL: "Dual Fuel",
    Fuel.OTHER_FOSSIL_FUELS: "Other Fossil Fuels",
}


class SimpleFuel(Enum):
    FOSSIL_FUEL = auto()
    RENEWABLE = auto()
    NUCLEAR = auto()


MEMBERS: Dict[SimpleFuel, Set[Fuel]] = {
    SimpleFuel.FOSSIL_FUEL: {Fuel.NATURAL_GAS, Fuel.DUAL_FUEL, Fuel.OTHER_FOSSIL_FUELS},
    SimpleFuel.RENEWABLE: {Fuel.HYDRO, Fuel.WIND, Fuel.OTHER_RENEWABLES},
    SimpleFuel.NUCLEAR: {Fuel.NUCLEAR},
}
