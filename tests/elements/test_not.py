from human_re import Digit, Literal, Not


def test_not():
    assert Not(Literal("a")).compile().pattern == "((?!a).*)"
    assert Not(Digit()).compile().pattern == "\D"
    assert Not(Not(Literal("aaa"))).compile().pattern == "aaa"
