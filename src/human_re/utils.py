import re


def str_is_char(s: str) -> bool:
    """
    Checks if the input string `s` contains exactly one character.
    """
    return len(str(s)) == 1


def char_is_a_to_z(s: str) -> bool:
    """
    Checks if the input string `s` is a single character from the English alphabet (case-insensitive).
    """
    return re.match(r"[a-zA-Z]", s) is not None


def int_is_digit(i: int) -> bool:
    """
    Checks if the input integer `i` is a single-digit number.
    """
    return len(str(i)) == 1
