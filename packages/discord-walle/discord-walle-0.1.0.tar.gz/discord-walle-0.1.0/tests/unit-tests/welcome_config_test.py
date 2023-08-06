from walle.core import UserNameType
from walle.configs import WelcomeConfig

import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "key": "username",
                "value": "rube",
                "name": "dummy-type",
            },
            "Welcome to the server, rube!",
        ),
    ],
)
def test_eval(test_input, expected):
    got = UserNameType(**test_input)
    types = [got]
    got = WelcomeConfig(types)
    assert str(got) == expected
