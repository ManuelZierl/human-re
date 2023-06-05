from human_re import Digit, Literal, Optional


def test_optional_compile():
    assert Optional(Literal("abc")).compile().pattern == "(abc)?"
    assert Optional(Digit()).compile().pattern == "(\d)?"
    assert Optional(Digit(), name="a_digit").compile().pattern == "(?P<a_digit>(\d)?)"
