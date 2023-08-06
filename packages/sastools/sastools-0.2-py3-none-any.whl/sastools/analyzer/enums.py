"""Enums used in the different analyzers."""

from enum import Enum, auto


class SAXSStandards(Enum):
    """Different standards used for calibration of SAXS data."""

    CHOLESTERYL_PALMITATE = auto()
    SILVER_BEHENATE = auto()


class LLCPhases(Enum):
    """Different known LLC phases."""

    H1 = "H1"
    V1 = "V1"
    LA = "La"
    INDETERMINATE = "indeterminate"


class LLCSpaceGroups(Enum):
    """Different space groups relevant for LLC phases."""

    P6MM = "P6mm"
    IA3D = "Ia3d"


class LLCMillerIndices(Enum):
    """Different miller indices relevant for LLC phases."""

    P6MM = ([1, 1, 2, 2, 3], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0])
    IA3D = ([1, 1, 2, 2, 2], [0, 1, 0, 1, 2], [0, 1, 0, 1, 2])
