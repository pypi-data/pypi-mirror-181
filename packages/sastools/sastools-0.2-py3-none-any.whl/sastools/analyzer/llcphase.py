"""ABC defining properties of different LLC phases."""

from enums import LLCPhases, LLCSpaceGroups
from abc import ABC, abstractmethod


class LLCPhase(ABC):
    """ABC defining the properties of an LLC Phase."""

    @abstractmethod
    def calculate_lattice_parameters(self, d_meas: list[float]):
        ...

    @property
    @abstractmethod
    def phase(self) -> LLCPhases:
        ...

    @property
    @abstractmethod
    def space_group(self) -> LLCSpaceGroups:
        ...

    @property
    @abstractmethod
    def miller_indices(self) -> tuple[list[int], list[int], list[int]]:
        ...

    @property
    @abstractmethod
    def lattice_parameters(self) -> list[float]:
        ...

    @property
    @abstractmethod
    def phase_information(self) -> dict:
        ...
