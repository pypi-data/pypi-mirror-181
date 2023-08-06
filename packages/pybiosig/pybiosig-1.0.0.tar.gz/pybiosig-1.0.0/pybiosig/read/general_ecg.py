"""
------------------------------------------------------------------------------------------
general ECG module
------------------------------------------------------------------------------------------
Sub-module to handle general aspects for reading ECG signals.

### Constants:
- ECG_NAMES     : list[str] : Standard names for 12-lead ECG signals.
- ECG_NAMES_EXT : list[str] : Extended 12-lead ECG signal names with vectorcardiogram (X,Y,Z).

### Functions:
- is_ECG()              : Checks if a signal identifier belongs to an ECG signal.
- normalize_ECG()       : Normalizes an ECG signal identifier.

### Author: 
Alejandro Alcaine Otín, Ph.D.
    lalcaine@usj.es"""

# DEPENDENCIES
import re

import pybiosig.read as pbread

# CONSTANTS AND FUNCTIONS

# Standard pattern for ECG name extraction (private use)
__ECG_PATTERN: str = "[ECKG_]*(\w+)[\(\d\)]*"

# Standard names for ECG signals
ECG_NAMES: list[str] = [
    "V1",
    "V2",
    "V3",
    "V4",
    "V5",
    "V6",
    "I",
    "II",
    "III",
    "aVR",
    "aVL",
    "aVF",
]
# Standard names for ECG signals + Vectorcardiogram
ECG_NAMES_EXT: list[str] = ECG_NAMES + ["X", "Y", "Z"]


def is_ECG(
    identifier: str, targets: list[str] = ECG_NAMES, pattern: str = __ECG_PATTERN
) -> bool:
    """Checks if a signal identifier belongs to an ECG signal accordingly to a list of
    target identifiers.

    Args:
        identifier (str): Signal identifier name.

        targets (list[str], optional): _description_.
        Defaults to ECG_NAMES.

        pattern (str, optional): Pattern (regex) to find in the identifier.
        Defaults to regex to find ECG signals.

    Returns:
        bool: Wether the identifier belongs or not to an ECG signal accordingly to the
        list of targets.
    """

    # Checking is in uppercase to avoid case-sensitive related errors
    return pbread.get_identifier(identifier.upper(), pattern) in map(str.upper, targets)


def normalize_ECG(
    identifier: str, targets: list[str] = ECG_NAMES, pattern: str = __ECG_PATTERN
) -> str | None:
    """Normalizes an ECG signal identifier accordingly to a list of target identifiers.

    Args:
        identifier (str): Signal identifier name.

        targets (list[str], optional): List of target identifiers.
        Defaults to ECG_NAMES.

        pattern (str, optional): Pattern (regex) to find in the identifier.
        Defaults to regex to find ECG signals.

    Returns:
        str | None:  Normalized identifier accordingly to a list of target identifiers.
        Returns None if the identifier do not belongs to an ECG signal
    """

    # Find out in uppercase
    if is_ECG(identifier, targets, pattern):
        extract = pbread.get_identifier(identifier, pattern)
        try:
            return targets[targets.index(extract)]
        except ValueError:  # Means that is an ECG but with uppercase match
            list_ECG_upper = [target.upper() for target in targets]
            return targets[list_ECG_upper.index(extract.upper())]

    return None
