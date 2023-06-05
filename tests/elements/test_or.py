import pytest

from human_re import Literal, Or


def test_or_validation():
    with pytest.raises(ValueError):
        Or(times=1)


def test_or_compile():
    assert (
        Or(Literal("ab"), Literal("cd"), Literal("ef")).compile().pattern
        == "(ab|cd|ef)"
    )

    assert (
        Or(Literal("ab"), Literal("cd"), Literal("ef"), times=2).compile().pattern
        == "(ab|cd|ef){2}"
    )

    assert (
        Or(Literal("ab"), Literal("cd"), times=2, name="ab_or_cd").compile().pattern
        == "(?P<ab_or_cd>(ab|cd){2})"
    )
