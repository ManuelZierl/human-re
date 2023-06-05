# Test case for str_is_char()
from src.utils import char_is_a_to_z, int_is_digit, str_is_char


def test_str_is_char():
    assert str_is_char("a") is True
    assert str_is_char("ab") is False


def test_char_is_a_to_z():
    assert char_is_a_to_z("A") is True
    assert char_is_a_to_z("b") is True
    assert char_is_a_to_z("ß") is False
    assert char_is_a_to_z("ü") is False
    assert char_is_a_to_z("1") is False


def test_int_is_digit():
    assert int_is_digit(5) is True
    assert int_is_digit(15) is False
