"""
------------------------------------------------------------------------------------------
general egm module
------------------------------------------------------------------------------------------
Sub-module to handle general aspects for reading EGM signals.

### Functions:
- maybe_EGM()           : Guess if signal identifier can be an EGM signal.
- extract_EGM()         : Extracts an EGM signal identifier following a pattern.

### Author: 
Alejandro Alcaine Otín, Ph.D.
    lalcaine@usj.es"""

# DEPENDENCIES
import pybiosig.read as pyread

# CONSTANTS 
# Standard pattern for EGM name extraction (private use)
__EGM_PATTERN = "^(\w+\s?\w+-\w+|\w+\s?\w+\,\w+|\w+\s?\w+\s?\w+?|\w+)[\(\d\)]*"

# FUNCTIONS
def maybe_EGM(identifier: str) -> bool:
    """Guess if signal identifier can be an EGM signal.

    Args:
        identifier (str): Signal identifier name.

    Returns:
        bool: Wether the identifier can be or not an EGM signal.
    """

    # If it is not an ECG, can be an EGM
    return not pyread.general_ecg.is_ECG(identifier, pyread.general_ecg.ECG_NAMES_EXT)


def extract_EGM(identifier: str, pattern: str = __EGM_PATTERN) -> str:
    """Extracts an EGM signal identifier following a pattern.

    Args:
        identifier (str): Signal identifier name.

        pattern (str, optional): Pattern (regex) to find in the identifier.
        Defaults to regex to find EGM signals.

    Returns:
        str: Extracted identifier following the pattern.
        Returns the input identifier if not an EGM or pattern does not match.
    """

    if maybe_EGM(identifier):
        extracted = pyread.get_identifier(identifier, pattern)
        if extracted:
            return extracted

    return identifier

