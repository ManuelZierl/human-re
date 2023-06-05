import pytest

from human_re import LiteralSet


def test_literal_set_validation():
    with pytest.raises(ValueError):
        LiteralSet()


def test_literal_set_compile():
    assert LiteralSet("abc", "###", "b#z").compile().pattern == "(abc|\\#\\#\\#|b\\#z)"
    assert LiteralSet("1", "qw", times=2).compile().pattern == "(1|qw){2}"
