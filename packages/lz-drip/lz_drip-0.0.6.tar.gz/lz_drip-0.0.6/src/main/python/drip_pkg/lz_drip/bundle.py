"""Define the Bundle class"""

import os
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

_V4_VERSION = "v4"
_DATA_CATEGORY = "DATA"
_DONE_CATEGORY = "DONE"
_META_DATA_CATEGORY = "METADATA"

_DONE_FILE_PATTERN = "v4*DONE*"
_SPADE_FILE_PATTERN = (
    "^("
    + _V4_VERSION
    + ")_([0-9]*)_("
    + _DATA_CATEGORY
    + "|"
    + _DONE_CATEGORY
    + "|"
    + _META_DATA_CATEGORY
    + ")_([^_]*)_(.*)$"
)
_VERSION_INDEX = 1
_TICKET_INDEX = _VERSION_INDEX + 1
_FILECATEGORY_INDEX = _TICKET_INDEX + 1
_REGISTRATION_INDEX = _FILECATEGORY_INDEX + 1
_PAYLOAD_INDEX = _REGISTRATION_INDEX + 1


def find_bundles(directory: Path):
    """
    Returns the list of Bundles in the specified directory
    """
    done_files = list(directory.glob(_DONE_FILE_PATTERN))
    result = []
    for done_file in done_files:
        result.append(Bundle(done_file))
    result.sort(key=_getmtime)
    return result


class Bundle:
    """
    This class gathers together the three files that make up a SPADE bundle.
    """

    def __init__(self, done_file: Path):
        """
        Creates an instance of this class.

        :param done_file: the Path to the DONE file of the bundle.
        """

        if not done_file.exists():
            raise ValueError("The supplied ' + _DONE_CATEGORY + ' file does not exist")
        parts = re.match(_SPADE_FILE_PATTERN, done_file.name)
        if parts is None:
            raise ValueError("The supplied file is not a DONE file")
        if parts.group(_FILECATEGORY_INDEX) != _DONE_CATEGORY:
            raise ValueError("The supplied file is not a DONE file")
        parent = done_file.parent
        self.__done_file = done_file
        self.__meta_file = parent.joinpath(
            parts.group(_VERSION_INDEX)
            + "_"
            + parts.group(_TICKET_INDEX)
            + "_"
            + _META_DATA_CATEGORY
            + "_"
            + parts.group(_PAYLOAD_INDEX)
            + ".meta.xml"
        )
        if not self.__meta_file.exists():
            raise ValueError(
                "The supplied ' + _META_DATA_CATEGORY + ' file does not exist"
            )

        self.__payload = parent.joinpath(
            parts.group(_VERSION_INDEX)
            + "_"
            + parts.group(_TICKET_INDEX)
            + "_"
            + _DATA_CATEGORY
            + "_"
            + parts.group(_PAYLOAD_INDEX)
            + ".root"
        )
        if not self.__payload.exists():
            raise ValueError("The supplied ' + _DATA_CATEGORY + ' file does not exist")

    def getmtime(self) -> float:
        """
        Returns the time stamp this object.
        """
        return os.path.getmtime(self.__done_file)

    def move(self, destination) -> None:
        """
        Moves the entire bundle from one directory to another
        """
        shutil.move(self.__payload, destination)
        shutil.move(self.__meta_file, destination)
        shutil.move(self.__done_file, destination)

    def move_to_canonical(self, destination) -> None:
        """
        Moves the entire bundle from one directory to another which is
        organized with respect to the bundle's canaonical_path.
        """
        tree = ET.parse(self.__meta_file)
        canonical_element = tree.find("canonical_path")
        if None is canonical_element:
            raise ValueError("No canonical_path in metadata")
        if None is canonical_element.text:
            raise ValueError("Empty canonical_path in metadata")
        canonical_path = Path(canonical_element.text)
        canonical_directory = canonical_path.parent
        warehouse_directory = destination.joinpath(canonical_directory)
        warehouse_directory.mkdir(parents = True,exist_ok=True)
        self.move(warehouse_directory)


def _getmtime(bundle: Bundle) -> float:
    """
    Returns the time stamp of the supplied bundle.
    """
    return bundle.getmtime()
