import pytest
from hypothesis import given
from hypothesis.strategies import floats, text

from box import Fruit


def test_fruit_init():
    fruit = Fruit("apple", 187)
    assert fruit.name == "apple"
    assert fruit.volume == 187


@pytest.mark.parametrize(
    "name,volume",
    [
        ("apple", 187),
        ("banana", 156.1),
        ("orange", 217.8),
    ],
)
def test_fruit_init_with_params(name: str, volume: float) -> None:
    fruit = Fruit(name, volume)
    assert fruit.name == name
    assert fruit.volume == volume


@given(text(), floats(allow_nan=False, allow_infinity=False))
def test_fruit_init_with_params_hypothesis(name: str, volume: float) -> None:
    fruit = Fruit(name, volume)
    assert fruit.name == name
    assert fruit.volume == volume


@pytest.mark.xfail(reason="Not implemented")
def test_fruit_init_validate_volume():
    with pytest.raises(ValueError) as exc_info:
        Fruit("apple", -1)
    assert str(exc_info.value) == "volume must be positive"


def test_fruit_str() -> None:
    fruit = Fruit("apple", 187)
    assert str(fruit) == "Fruit(name='apple', volume=187)"


def test_fruit_repr() -> None:
    fruit = Fruit("apple", 187)
    assert repr(fruit) == "Fruit(name='apple', volume=187)"
