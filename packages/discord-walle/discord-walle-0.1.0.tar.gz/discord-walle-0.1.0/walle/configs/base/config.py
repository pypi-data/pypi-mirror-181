from abc import ABCMeta, abstractmethod
from collections.abc import Iterable

__all__ = [
    "BaseConfig",
]


class BaseConfig(metaclass=ABCMeta):
    """Base Config"""

    def __init__(
        self,
        config_types,
        name="base-config",
    ):
        self.config_types = config_types
        if not isinstance(config_types, Iterable):
            if not isinstance(config_types, (list, tuple)):
                raise AssertionError(
                    f"Expected a valid config tpye of tuple or list, but got {type(config_types)}"
                )

        if "base" in name:
            raise AssertionError(
                f"Expected a valid name, but received base class name: {name}"
            )
        self.name = name

        self._parse_types()

    def _parse_types(self):
        """config types builder"""
        for __o in self.config_types:
            key = __o.key
            setattr(self, key, __o)

    def get_type(self, key):
        """getter method for snagging typed values"""
        return getattr(self, key)

    def set_type(self, __o, value):
        """setter to change a mutable attribute"""
        if __o.is_mutable:
            setattr(self, __o.key, value)
        else:
            print(
                f"Config got a request to change a immutable type {type.key} with {value}. It is not allowed"
            )

    @abstractmethod
    def __str__(self):
        """to string method"""
        pass
