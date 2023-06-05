from human_re import StartOfString


def test_start_of_string_compile():
    assert StartOfString().compile().pattern == "^"
