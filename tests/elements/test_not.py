from src import Digit
from src.elements.literal import Literal
from src.elements.not_ import Not


def test_not():
    assert Not(Literal("a")).compile().pattern == "((?!a).*)"
    assert Not(Digit()).compile().pattern == "\D"
    assert Not(Not(Literal("aaa"))).compile().pattern == "aaa"
