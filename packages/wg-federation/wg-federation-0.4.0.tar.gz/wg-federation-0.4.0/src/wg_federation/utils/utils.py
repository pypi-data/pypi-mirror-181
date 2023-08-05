import re
from collections.abc import MutableMapping, MutableSet, MutableSequence, Sequence
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Union, Callable

from typing.io import IO


class Utils:
    """
    Contains reusable utility code.
    This class only contains short, static methods.
    """

    @staticmethod
    def classname(instance: object) -> str:
        """
        Display the class name of a given object instance
        :param instance: Instance to get the class from
        :return:
        """
        return f'{instance.__class__.__name__}♦'

    @staticmethod
    def always_dict(instance: Any) -> dict:
        """
        Takes any argument. Returns it unmodified if it’s a, otherwise, return empty dict
        :param instance: anything
        :return: instance if instance is dict, otherwise {}
        """
        if not isinstance(instance, dict):
            return {}

        return instance

    @staticmethod
    def has_extension(path_or_file: Union[str, TextIOWrapper], extension: str) -> bool:
        """
        Check that a path has a given extension.
        :param path: path to check
        :param extension: extension to check against the path. Can be a regular expression.
        :return: True if the path has extension, False otherwise
        """
        if isinstance(path_or_file, TextIOWrapper):
            path_or_file = path_or_file.name

        return bool(re.match(fr'^\.{extension}$', Path(path_or_file).suffix, re.IGNORECASE))

    @staticmethod
    def recursive_map(callback: Callable[[Any], Any], data_ref) -> Sequence:
        """
        Apply a callback function on all the element of data_ref
        Careful, this function mutates data_ref in memory.
        :param callback: Function that transforms its only argument
        :param data_ref: Iterable to be processed
        :return: The modified data_ref
        """
        for key in data_ref.keys() if isinstance(data_ref, MutableMapping) else range(len(data_ref)):
            data_ref[key] = callback(data_ref[key])

            if isinstance(data_ref[key], (MutableMapping, MutableSet, MutableSequence)):
                Utils.recursive_map(callback, data_ref[key])

        return data_ref

    @staticmethod
    def open(file: str, mode: str, encoding: str) -> IO:
        """
        Opens a files.
        This method simplifies mocking of the builtins.open
        :param file:
        :param mode: Among normal "open" modes, adds a 'a++' that acts like 'a+' but also creates parent path.
        :param encoding:
        :return:
        """
        if 'a++' == mode:
            # pathlib is badly made and thus untestable
            Path(file).parents[0].mkdir(parents=True, exist_ok=True)
            mode = 'a+'

        return open(file=file, mode=mode, encoding=encoding)
