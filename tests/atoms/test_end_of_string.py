from human_re import EndOfString


def test_end_of_string_compile():
    assert EndOfString().compile().pattern == "$"
