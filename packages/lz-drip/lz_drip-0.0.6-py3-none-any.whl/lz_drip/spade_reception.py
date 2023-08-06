"""Define the FileDropper class"""

from typing import List, Tuple

from drip import Dropper
from .bundle import find_bundles, Bundle, _DONE_FILE_PATTERN
from .file_utils import (
    read_config,
    select_source,
    select_destination,
    select_threshold,
)


class SpadeReception(Dropper):
    """
    This class provides the concrete implementation use by a Feeder
    instance to copy SPADE bundles from one directory to another.
    """

    def __init__(self, config_file: str, section: str):
        """
        Creates an instance of this class.

        :param source: the Path to the source directory
        :param destination: the Path to the destination directory
        """
        config = read_config(config_file, section)

        self.__src = select_source(config)
        self.__dst = select_destination(config)
        self.__threshold = select_threshold(config)

    def assess_condition(self) -> Tuple[int, str]:
        """
        Assess whether a drip should be executed or not.

        :return maximum number if items that can be dropped and
        explanation of any limitations.
        """
        count = len(list(self.__dst.glob(_DONE_FILE_PATTERN)))
        if 1 == count:
            multiple = ""
            plural = ""
        else:
            multiple = "some of "
            plural = "s"
        if count >= self.__threshold:
            return (
                0,
                f"{multiple}the {count} bundle{plural} in the target directory to be handled",
            )
        return self.__threshold - count, ""

    def drop(self, item):
        """
        "Drops" the supplied item, i.e. acts on that item.
        """
        item.move(self.__dst)

    def fill_cache(self) -> List[Bundle]:
        """
        Fills internal list of bundles to be moved.
        """
        return find_bundles(self.__src)
