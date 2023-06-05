from human_re import Newline


def test_newline_compile():
    assert Newline().compile().pattern == "\\n"
    assert Newline(times=3).compile().pattern == "\\n{3}"
    assert (
        Newline(times=3, name="three_newlines").compile().pattern
        == "(?P<three_newlines>\\n{3})"
    )
