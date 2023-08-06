"""
-----------------------------------------------------------------------------------------
Read module
-----------------------------------------------------------------------------------------
Module for reading signals.

### Sub-modules:
- general_ecg : Sub-module to handle general aspects for reading ECG signals.
- general_egm : Sub-module to handle general aspects for reading EGM signals.
- read_carto  : Sub-module to read CARTO signals and metadata

### Functions:
- get_identifier()      : Gets a signal identifier by matching a pattern.
- rename_ECG_and_EGM()  : Rename appropriately ECG and EGM identifiers.

### Version: 0.1.0

### Author: 
Alejandro Alcaine Otín, Ph.D.
    lalcaine@usj.es"""

# DEPENDENCIES
import re

# MODULE VERSION
__version__ = "0.1.0"

# IMPORTS
import pybiosig.read.general_ecg as general_ecg
import pybiosig.read.general_egm as general_egm
import pybiosig.read.read_carto as read_carto

# MODULE FUNCTIONS
def get_identifier(
    identifier: str, pattern: str = general_ecg.__ECG_PATTERN
) -> str:
    """Gets a signal identifier by matching a pattern.

    Args:
        identifier (str): Signal identifier name.

        pattern (str, optional): Pattern (regex) to find in the identifier.
        Defaults to regex to find ECG signals.

    Returns:
        str: Extracted identifier.
        Returns empty str when no identifier is found.
    """

    return re.findall(pattern, identifier)[0]


def rename_ECG_and_EGM(
    identifier: str,
    ecg_targets: list[str] = general_ecg.ECG_NAMES_EXT,
    ecg_pattern: str = general_ecg.__ECG_PATTERN,
    egm_pattern: str = general_egm.__EGM_PATTERN,
) -> str:
    """Rename appropriately ECG and EGM identifiers.

    Args:
        identifier (str): Signal identifier name.

        ecg_targets (list[str], optional): List of target identifiers.
        Defaults to ECG_NAMES_EXT.

        ecg_pattern (str, optional): ECG pattern (regex) to find in the identifier.
        Defaults to regex to find ECG signals.

        egm_pattern (str, optional): EGM pattern (regex) to find in the identifier.
        Defaults to regex to find EGM signals.

    Returns:
        str: Renamed identifier following rules.
        Returns the untouched identifier if no rename can be made.
    """

    rename = general_ecg.normalize_ECG(
        identifier, ecg_targets, ecg_pattern
    )

    return (
        general_egm.extract_EGM(identifier, egm_pattern)
        if rename is None
        else rename
    )
