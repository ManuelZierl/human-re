import pytest

from human_re import Digit


def test_digit_validation():
    with pytest.raises(ValueError):
        Digit(2, 1)

    with pytest.raises(ValueError):
        Digit(0, 10)

    with pytest.raises(ValueError):
        Digit(10, 11)


def test_digit_init():
    assert Digit().start == 0
    assert Digit().stop == 9
    assert Digit().times == 1


def test_digit_compile():
    assert Digit().compile().pattern == r"\d"
    assert Digit(1, 9).compile().pattern == r"[1-9]"
    assert Digit(2, 8).compile().pattern == r"[2-8]"
    assert Digit(2, 8, times=3).compile().pattern == r"[2-8]{3}"
    assert Digit(3, 3).compile().pattern == r"3"
    assert Digit(3, 3, times=3).compile().pattern == r"3{3}"
