"""Provide utilities to help using the lz_drip package"""

import os
from pathlib import Path

from drip import utils as drip_utils

_CONFIG_STRINGS = ["source", "destination"]
_SOURCE_INDEX = 0
_DESTINATION_INDEX = 1
_CONFIG_INTEGERS = ["threshold"]
_THRESHOLD_INDEX = 0

_DEFAULT_THRESHOLD = 8


def read_config(config_file, section) -> drip_utils.Configs:
    """
    Reads the supplied configuration ini

    :param config_file: the path to the file containing the configuration information.
    :param section: the section within the file containing the configuration for this instance.
    """
    return drip_utils.read_config(
        config_file, section, integers=_CONFIG_INTEGERS, strings=_CONFIG_STRINGS
    )


def select_source(config) -> Path:
    """
    Returns the Path to the selected file source
    """
    drip_source = os.getenv("FILE_DRIP_SOURCE")
    if None is drip_source:
        drip_source = str(config[_CONFIG_STRINGS[_SOURCE_INDEX]])
    if None is drip_source:
        raise ValueError(
            "source must be defined in configuration file,"
            + " or envar FILE_DRIP_SOURCE set"
        )
    source = Path(drip_source)
    if not source.exists():
        raise ValueError(f"{source.resolve()} does not exist!")
    return source


def select_destination(config) -> Path:
    """
    Returns the Path to the selected file destination
    """
    drip_destination = os.getenv("FILE_DRIP_DESTINATION")
    if None is drip_destination:
        drip_destination = str(config[_CONFIG_STRINGS[_DESTINATION_INDEX]])
    if None is drip_destination:
        raise ValueError(
            "destination must be defined in configuration file,"
            + " or envar FILE_DRIP_DESTINATION set"
        )
    destination = Path(drip_destination)
    if not destination.exists():
        raise ValueError(f"{destination.resolve()} does not exist!")
    if not destination.is_dir():
        raise ValueError(f"{destination.resolve()} is not a directory")
    return destination


def select_threshold(config) -> int:
    """
    Returns the Path to the selected file threshold
    """
    drip_threshold = os.getenv("FILE_DRIP_THRESHOLD")
    if None is drip_threshold:
        threshold: int = int(config[_CONFIG_INTEGERS[_THRESHOLD_INDEX]])
        if None is threshold:
            return _DEFAULT_THRESHOLD
        return threshold
    return int(drip_threshold)
