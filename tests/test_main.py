import pytest

from main import greeting


@pytest.mark.parametrize(
    "name, expected",
    [
        ("World", "Hello, World"),
        ("Username", "Hello, Username"),
    ],
)
def test_greeting(name: str, expected: str) -> None:
    assert greeting(name) == expected
