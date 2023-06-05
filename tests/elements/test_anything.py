from human_re import Anything, Range


def test_anything_compile():
    assert Anything().compile().pattern == "."
    assert Anything(times=5).compile().pattern == ".{5}"
    assert Anything(times=Range(1, ...), name="any").compile().pattern == "(?P<any>.+)"
