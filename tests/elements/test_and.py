from human_re import And, Digit


def test_and_compile():
    assert And(Digit(0, 8), Digit(4, 9)).compile().pattern == "((?=[0-8])[4-9])"
    assert (
        And(Digit(0, 8), Digit(4, 9), name="and").compile().pattern
        == "(?P<and>((?=[0-8])[4-9]))"
    )
    assert (
        And(Digit(0, 8), Digit(4, 9), times=2).compile().pattern
        == "((?=[0-8])[4-9]){2}"
    )
