from human_re import Literal, Named


def test_named_compile():
    assert Named(Literal("a"), name="itsa").compile().pattern == "(?P<itsa>a)"
    assert Named(Literal("a")).compile().pattern == "a"
