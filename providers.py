import os
from typing import Any
import json
from .exceptions import VariableNotFoundError


class AbstractProvider:
    """Implement this class and pass to `field`"""

    def get(self, name: str) -> Any:
        """Return a value or None"""
        raise NotImplementedError()


class EnvironmentProvider(AbstractProvider):
    """Default provider. Gets vals from environment"""

    def get(self, name: str) -> Any:
        try:
            return os.environ[name]
        except KeyError:
            raise VariableNotFoundError(name)


class JsonProvider(AbstractProvider):
    """
    Gets value from json file
    """
    def __init__(self, *args, file_path: str, **kwargs):
        self._dump_data = self._read_json(*args, file_path, **kwargs)

    @staticmethod
    def _read_json(*args, file_path, **kwargs):
        with open(file_path, 'r', *args, **kwargs) as file:
            return json.load(file)

    def get(self, name: str) -> Any:
        try:
            return self._dump_data[name]
        except KeyError:
            raise VariableNotFoundError(name)


DEFAULT_PROVIDER = EnvironmentProvider()
