from .base import BaseConfig
from walle.core import constants

__all__ = [
    "WelcomeConfig",
]


class WelcomeConfig(BaseConfig):
    """"""

    def __init__(
        self,
        config_types,
        name="welcome-config",
    ):
        super().__init__(
            config_types=config_types,
            name=name,
        )

    def _welcome_message(self):
        __o = self.get_type(constants.USERNAME)
        return f"Welcome to the server, {__o.value}!"

    def __str__(self):
        return self._welcome_message()
