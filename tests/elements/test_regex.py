import pytest

from human_re import Literal, Regex


def test_regex_validation():
    with pytest.raises(ValueError):
        Regex(times=1)


def test_regex_compile():
    assert Regex(Literal("a"), Literal("bc"), times=3).compile().pattern == "(abc){3}"

    assert (
        Regex(Literal("a"), Literal("bc"), times=3, name="my_regex").compile().pattern
        == "(?P<my_regex>(abc){3})"
    )

    assert (
        Regex(Literal("a"), Literal("bc"), match_start=True).compile().pattern
        == "^(abc)"
    )

    assert (
        Regex(Literal("a"), Literal("bc"), match_end=True).compile().pattern == "(abc)$"
    )
