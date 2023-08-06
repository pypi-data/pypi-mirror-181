"""Different space groups and their properties needed for analyzers."""

from enums import LLCPhases, LLCSpaceGroups, LLCMillerIndices
from llcphase import LLCPhase

import numpy as np


class HexagonalPhase(LLCPhase):
    """Container for properties of hexagonal LLC phases."""

    def __init__(self, space_group: LLCSpaceGroups) -> None:
        """Pass the determined space group as LLCSpaceGroups.

        Args:
            space_group (LLCSpaceGroups): Space group of hexagonal phase.
        """
        self._phase = LLCPhases.H1
        self._space_group = space_group
        self._miller_indices = ()
        self._lattice_parameters = []
        self._phase_information = {}

    def __repr__(self) -> str:
        return "Hexagonal LLC Phase"

    def _calculate_a_H1(self, d: float, h: int, k: int) -> float:
        # Calculate and return the lattice parameter for a given lattice
        # plane distance d, miller index h, and miller index k.
        a_H1 = d * np.sqrt((4 / 3) * ((h**2 + k**2 + (h * k))))
        return a_H1

    def calculate_lattice_parameters(self, d_meas: list[float]) -> None:
        """Calculate lattice parameters of hexagonal phase using a list
        of measured lattice plane distances `d_meas`.

        Args:
            d_meas (list[float]): Measured lattice plane distances.
        """
        for i, j in enumerate(d_meas):
            a_i = self._calculate_a_H1(
                d_meas[i], self.miller_indices[0][i], self.miller_indices[1][i]
            )
            self.lattice_parameters.append(a_i)

    @property
    def phase(self) -> LLCPhases:
        """Get hexagonal phase."""
        return self._phase

    @property
    def space_group(self) -> LLCSpaceGroups:
        """Get space group of hexagonal phase."""
        return self._space_group

    @property
    def miller_indices(self) -> tuple[list[int], list[int], list[int]]:
        """Get miller indices of hexagonal phase."""
        self._miller_indices = LLCMillerIndices[self._space_group.name].value
        return self._miller_indices

    @property
    def lattice_parameters(self) -> list[float]:
        """Get lattice parameters of hexagonal phase."""
        return self._lattice_parameters

    @property
    def phase_information(self) -> dict:
        """Get full phase information of hexagonal phase."""
        self._phase_information = dict(
            phase=self.phase.value,
            lattice_parameter=np.mean(self.lattice_parameters),
        )
        return self._phase_information


class CubicPhase(LLCPhase):
    """Container for properties of cubic LLC phases."""

    def __init__(self, space_group: LLCSpaceGroups) -> None:
        """Pass the determined space group as LLCSpaceGroups.

        Args:
            space_group (LLCSpaceGroups): Space group of cubic phase.
        """
        self._phase = LLCPhases.V1
        self._space_group = space_group
        self._miller_indices = ()
        self._lattice_parameters = []
        self._phase_information = {}
        self._d_reciprocal = []
        self._sqrt_miller = []

    def __repr__(self) -> str:
        return f"Cubic ({self.phase.value}) LLC Phase"

    def _calculate_a_V1(self, d: float, h: int, k: int, l: int) -> float:
        # Calculate and return the lattice parameter for a given lattice
        # plane distance d, miller index h, k, and l.
        a_V1 = d * (np.sqrt((h**2) + (k**2) + (l**2)))
        return a_V1

    def calculate_lattice_parameters(self, d_meas: list[float]) -> None:
        """Calculate lattice parameters of cubic phase using a list of
        measured lattice plane distances `d_meas`.

        Args:
            d_meas (list[float]): Measured lattice plane distances.
        """
        for i, j in enumerate(d_meas):
            a_i = self._calculate_a_V1(
                d_meas[i],
                self.miller_indices[0][i],
                self.miller_indices[1][i],
                self.miller_indices[2][i],
            )
            self._lattice_parameters.append(a_i)

    @property
    def phase(self) -> LLCPhases:
        """Get cubic phase."""
        return self._phase

    @property
    def space_group(self) -> LLCSpaceGroups:
        """Get space group of cubic phase."""
        return self._space_group

    @property
    def miller_indices(self) -> tuple[list[int], list[int], list[int]]:
        """Get miller indices of cubic phase."""
        self._miller_indices = LLCMillerIndices[self._space_group.name].value
        return self._miller_indices

    @property
    def lattice_parameters(self) -> list[float]:
        """Get lattice parameters of cubic phase."""
        return self._lattice_parameters

    @property
    def phase_information(self) -> dict:
        """Get full phase information of cubic phase."""
        self._phase_information = dict(
            phase=self.phase.value,
            lattice_parameter=np.mean(self.lattice_parameters),
        )
        return self._phase_information

    @property
    def d_reciprocal(self) -> list[float]:
        """Get reciprocal lattice plane distances of cubic phase."""
        return self._d_reciprocal

    @d_reciprocal.setter
    def d_reciprocal(self, values: list[float]) -> None:
        self._d_reciprocal = values

    @property
    def sqrt_miller(self) -> list[int]:
        """Get square roots of miller indices of cubic phase."""
        return self._sqrt_miller

    @sqrt_miller.setter
    def sqrt_miller(self, values: list[int]) -> None:
        self._sqrt_miller = values


class LamellarPhase(LLCPhase):
    """Container for properties of lamellar LLC phases."""

    def __init__(self) -> None:
        self._phase = LLCPhases.LA
        self._space_group = None
        self._miller_indices = None
        self._lattice_parameters = []
        self._phase_information = {}

    def __repr__(self) -> str:
        return "Lamellar LLC Phase"

    def calculate_lattice_parameters(self, d_meas: list[float]) -> None:
        """Calculate lattice parameters of lamellar phase using a list
        of measured lattice plane distances `d_meas`.

        Args:
            d_meas (list[float]): Measured lattice plane distances.
        """
        self._lattice_parameters.append[d_meas[0]]

    @property
    def phase(self) -> LLCPhases:
        """Get lamellar phase."""
        return self._phase

    @property
    def space_group(self) -> None:
        """Get space group of lamellar phase."""
        return self._space_group

    @property
    def miller_indices(self) -> None:
        """Get miller indices of lamellar phase."""
        return self._miller_indices

    @property
    def lattice_parameters(self) -> list[float]:
        """Get lattice parameters of lamellar phase."""
        return self._lattice_parameters


class IndeterminatePhase(LLCPhase):
    """Container for properties of indeterminate LLC phases."""

    def __init__(self) -> None:
        self._phase = LLCPhases.INDETERMINATE
        self._space_group = None
        self._miller_indices = None
        self._lattice_parameters = None
        self._phase_information = {}

    def __repr__(self) -> str:
        return "Indeterminate LLC Phase"

    def calculate_lattice_parameters(self, d_meas: list[float]) -> None:
        """Do not use this method! Indeterminate phases have no lattice
        parameters.

        Args:
            d_meas (list[float]): Measured lattice plane distances.

        Raises:
            NotImplementedError: If this method is called.
        """
        raise NotImplementedError(
            f"No lattice parameter in indeterminate phases!"
        )

    @property
    def phase(self) -> LLCPhases:
        """Get indeterminate phase."""
        return self._phase

    @property
    def space_group(self) -> None:
        """Get space group of indeterminate phase."""
        return self._space_group

    @property
    def miller_indices(self) -> None:
        """Get miller indices of indeterminate phase."""
        return self._miller_indices

    @property
    def lattice_parameters(self) -> None:
        """Get lattice parameters of indeterminate phase."""
        return self._lattice_parameters

    @property
    def phase_information(self) -> dict:
        """Get full phase information of indeterminate phase."""
        self._phase_information = dict(
            phase=self.phase.value,
            lattice_parameter="-",
        )
        return self._phase_information
