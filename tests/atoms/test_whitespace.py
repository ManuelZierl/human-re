from human_re import Not, Whitespace


def test_whitespace_compile():
    assert Whitespace().compile().pattern == "\s"
    assert Whitespace(name="white").compile().pattern == "(?P<white>\s)"
    assert Whitespace(name="white", times=5).compile().pattern == "(?P<white>\s{5})"


def test_not_whitespace():
    assert Not(Whitespace()).compile().pattern == "\S"
    assert Not(Whitespace(name="white")).compile().pattern == "(?P<white>\S)"
    assert (
        Not(Whitespace(name="white", times=5)).compile().pattern == "(?P<white>\S{5})"
    )
