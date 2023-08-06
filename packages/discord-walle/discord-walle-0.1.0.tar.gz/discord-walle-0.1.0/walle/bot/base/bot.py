from abc import ABCMeta, abstractmethod

__all__ = [
    "BaseBot",
]


class BaseBot(metaclass=ABCMeta):
    """Base Bot"""

    def __init__(
        self,
        event_config,
        action_config,
        name="base-bot",
    ):
        self.event_config = event_config
        self.action_config = action_config
        self.name = name
        if name.contains("base"):
            with AssertionError as msg:
                print(msg, "Expected new bot class name but got: ", self.name)

    @abstractmethod
    def handle_event(self, event):
        """ """
        pass

    @abstractmethod
    def handle_action(self, action):
        """ """
        pass

    @abstractmethod
    def _parse_event_tokens(self, tokens, **kwargs):
        """ """
        pass

    @abstractmethod
    def _parse_action_tokens(self, tokens, **kwargs):
        """ """
        pass
