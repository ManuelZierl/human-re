import re

from human_re import RegexPattern


def test_regex_patter_compile():
    assert RegexPattern(re.compile("#abc\d")).compile().pattern == "#abc\d"
