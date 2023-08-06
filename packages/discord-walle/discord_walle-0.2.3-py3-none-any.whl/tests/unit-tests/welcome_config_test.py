from walle.configs import WelcomeConfig

import pytest


class Member:
    def __init__(
        self,
        name,
        id=0,
        bot=False,
    ):
        self.name = "rube"
        self._name = name
        self.bot = bot
        self.id = id
        self.__name__ = "Member"


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "name": "dummy-type",
            },
            "Welcome to the server, rube!",
        ),
    ],
)
def test_eval(test_input, expected):
    got = Member(**test_input)
    got = WelcomeConfig(got)
    assert str(got) == expected
