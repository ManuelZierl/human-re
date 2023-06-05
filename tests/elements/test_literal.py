import pytest

from human_re import Literal


def test_literal_validation():
    with pytest.raises(ValueError):
        Literal("")


def test_literal_compile():
    assert Literal("a").compile().pattern == "a"
    assert Literal("?").compile().pattern == "\\?"
    assert Literal("#").compile().pattern == "\\#"
