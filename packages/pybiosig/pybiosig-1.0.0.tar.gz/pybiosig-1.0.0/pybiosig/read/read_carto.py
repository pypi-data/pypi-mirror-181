"""
-------------------------------------------------------------------------------------------------
read_carto module
-------------------------------------------------------------------------------------------------
Sub-module to read CARTO signals and metadata.

### Constants:
- CAR_DEFAULT     : Dictionary with common "*_car.txt" file columns to choose.

### Functions:
- read_car_file()   : Parses "*_car.txt" files from CARTO exports.
- read_signal()     : Reads CARTO signal data and metadata.

CARTO(r) is a trademark of BioSense Webster Inc.

### Author: 
Alejandro Alcaine Otín, Ph.D.
    lalcaine@usj.es"""

# DEPENDENCIES
import os
import re
from typing import Any

import pandas as pd

import pybiosig.read as pbread
from pybiosig.signal import Signal

# CONSTANTS AND FUNCTIONS

# Pattern for extract map name and point number from filename (private use)
__MAP_POINT: str = "^(.+)_P(\d+)_.+$"
# Pattern for version extraction (private use)
__VERSION: str = "ECG_Export_(\d*\.\d+|\d+)"
# Pattern for gain extraction in V3 o V4+ CARTO recordings (private use)
__GAIN_V3: str = "=\s(\d*\.\d+|\d+)"
__GAIN_V4: str = "=\s(\d+\.\d+|\d+)\n?"
# Pattern for reference signal extraction in V4+ CARTO recordings (private use)
__REFERENCES_V4: str = "(Unipolar|Bipolar|Reference)\s+\w*\s*?Channel=(\w+\-\w+|\w+)"

# Common CARTO data to be read
CAR_DEFAULT: dict[str, int] = {
    "number": 3,
    "pos_X": 5,
    "pos_Y": 6,
    "pos_Z": 7,
    "v_uni": 11,
    "v_bip": 12,
    "LAT": 13,
    "tag": 16,
}


def read_car_file(
    file_path: str, info: dict[str, int] = CAR_DEFAULT
) -> pd.DataFrame | int:
    """Parses "*_car.txt" files from CARTO exports.

    Args:
        file_path (str): Path to the *_car.txt file to be read.

        info (dict[str,int], optional): Dictionary to rename columns in the
        resulting DataFrame. Values of the dictionary must start at 1.
        Defaults to CAR_DEFAULT.

    Returns:
        pd.DataFrame | int: Pandas DataFrame with requested information.

        Returns -1 if any error happens.
    
    CARTO(r) is a trademark of BioSense Webster Inc.
    """
    try:
        if isinstance(info, dict):
            car_data = pd.read_table(
                file_path,
                skiprows=1,
                sep="\t",
                header=None,
                usecols=[col - 1 for col in info.values()],
            )

            car_data.rename(
                columns={value - 1: key for key, value in info.items()}, inplace=True
            )
        else:
            car_data = pd.read_table(file_path, skiprows=1, sep="\t", header=None)

        return car_data
    except Exception as error:
        print(f"Error: {str(error)}")
        return -1


def read_signal(
    file_path: str, delimiter: str = "\s+", **kargs: dict[str, Any]
) -> Signal | int:
    """Reads CARTO signal data and metadata.

    Args:
        file_path (str): Path to the signal file (".txt") to be read.

        delimiter (str, optional): Text delimiter (regex) to be use for reading the data.
        Defaults to "\s+".

        kargs (dict[str,Any], optional): keywords arguments to control export. 
        Accepted keywords and funtionality:
           - custom_sf (int): Allows to define a personalized sampling frequency of the signal. Defaults to Signal.sf = 1000.
           - export_all (bool): Force to export all the signals when parsing CARTO V4+ recordings.
            Default to False: export only reference + ECG signals.
           - references_V3 (list[str]): Allows to choose the signals to be exported in V3 recordings (includes also all ECG signals).
            Defaults to export all signals without reference attributes.
           - car_data (pd.DataFrame): Pre-loaded CARTO "_car.txt" DataFrame. This may improve performace in signal reading.
            Defaults to None: calls read_car_file().

    Raises:
        NotImplementedError: Unsupported CARTO ECG_Export file version.

    Returns:
        Signal | int: Signal object with exported data.

        Returns -1 if signal cannot be read.

    CARTO(r) is a trademark of BioSense Webster Inc.
    """
    
    # Setting the metadata dictionary
    meta = {"sf": 1000}  # CARTO records are "usually" sampled at 1000 Hz
    if "custom_sf" in kargs:
        meta["sf"] = kargs["custom_sf"]

    # fmt: off (force formatter no to split this)
    # Get map name and point number from filename 
    meta["map_name"], meta["point_num"] = re.findall(__MAP_POINT, os.path.split(file_path)[1])[0]
    # fmt: on

    # Get information and signal data from file
    try:
        with open(file_path, "r") as f:
            # This line needs to be preserved for V3 gain extraction
            line = f.readline()
            version = float(re.findall(__VERSION, line)[0])

            if version >= 4:  # Version 4+
                # Gain is in next line
                meta["gain"] = float(re.findall(__GAIN_V4, f.readline())[0])

                selected_signals = []  # This is for returning only those signals + ECG
                for mode, reference in re.findall(__REFERENCES_V4, f.readline()):
                    meta[f"{mode.lower()}_mapping"] = reference
                    selected_signals.append(reference)

            elif version == 3:  # Gain is in version line
                meta["gain"] = float(re.findall(__GAIN_V3, line)[0])
            else:
                raise NotImplementedError(
                    f"Not supported ECG_Export file version {version:0.2f}."
                )

        if version >= 4:
            # Data is stored as integer for memory efficiency
            signal = pd.read_table(
                file_path, sep=delimiter, skiprows=3, header=0, dtype=int
            )  
        else:  # version 3
            # Data is stored as integer for memory efficiency
            signal = pd.read_table(
                file_path, sep=delimiter, skiprows=1, header=0, dtype=int
            )  

        # Rename signal identifiers
        signal.rename(
            columns={col: pbread.rename_ECG_and_EGM(col) for col in signal.columns},
            inplace=True,
        )

        # In V4 onwards only returns ECG + _mapping signals
        if version >= 4 and not ("export_all" in kargs and kargs["export_all"]):
            signal = signal[list(set(selected_signals + pbread.general_ecg.ECG_NAMES))]
        # In V3, we can setup manually the selected signals with "references_V3"
        elif version == 3 and "references_V3" in kargs:
            signal = signal[list(set(kargs["references_V3"] + pbread.general_ecg.ECG_NAMES))]

            for reference in kargs["references_V3"]:
                if reference in signal.columns:
                    if pbread.general_ecg.is_ECG(reference):
                        meta["reference_mapping"] = reference
                    elif "-" in reference:
                        meta["reference_bipolar"] = reference
                    else:
                        meta["reference_unipolar"] = reference


        meta["channels"] = list(signal.columns)

        # Reading extra information from _car.txt file
        if "car_data" in kargs and "number" in kargs["car_data"].columns:
            car_data = kargs["car_data"]
        else:
            car_data = read_car_file(
                os.path.join(
                    os.path.split(file_path)[0], f'{meta["map_name"]}_car.txt'
                ),
                CAR_DEFAULT,
            )

        car_data = car_data[car_data["number"] == int(meta["point_num"])]
        for data in car_data.columns:
            if data != "number":
                meta[data] = car_data.iloc[0][data]
        

        return Signal(signal.to_numpy(),**meta)
    except Exception as error:
        print(f"Error: {str(error)}")
        return -1
