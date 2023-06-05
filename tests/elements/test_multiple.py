import pytest

from human_re import Literal, Multiple, Range, SpecialQuantifier


def test_range_validation():
    with pytest.raises(TypeError):
        Range("0", 1)

    with pytest.raises(TypeError):
        Range(0, "1")

    with pytest.raises(ValueError):
        Range(1, 0)


def test_range_compile_quantifier():
    assert Range(0, 1).compile_quantifier() == "?"
    assert Range(0, ...).compile_quantifier() == "*"
    assert Range(1, ...).compile_quantifier() == "+"
    assert Range(3, ...).compile_quantifier() == "{3,}"
    assert Range(2, 10).compile_quantifier() == "{2,10}"
    assert Range(3, 3).compile_quantifier() == "{3}"
    assert Range(1, 1).compile_quantifier() == ""


def test_multiple_compile():
    assert Multiple(Literal("a"), times=2).compile().pattern == "a{2}"

    assert Multiple(Literal("a"), times=(7, 10)).compile().pattern == "(a{10}|a{7})"

    assert Multiple(Literal("a"), times=Range(0, ...)).compile().pattern == "a*"

    assert Multiple(Literal("a"), times=Range(7, 10)).compile().pattern == "a{7,10}"

    assert Multiple(Literal("a"), times=1).compile().pattern == "a"

    assert (
        Multiple(Literal("a"), times=SpecialQuantifier.LAZY).compile().pattern == "a*?"
    )

    assert Multiple(Literal("a"), times=Range(1, 1)).compile().pattern == "a"

    assert (
        Multiple(Literal("a"), times=(7, 10), name="seven_or_ten_as").compile().pattern
        == "(?P<seven_or_ten_as>(a{10}|a{7}))"
    )
