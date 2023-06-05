from human_re import EndOfString, Integer, Regex, StartOfString


def test_regex_0_to_compile():
    assert (
        Integer._regex_0_to("102").compile().pattern
        == "((0\d{1,2})|(1((0[0-2])|\d))|\d{1,2})"
    )


def test_regex_larger_than_compile():
    assert (
        Integer._regex_larger_than("192").compile().pattern
        == "(([2-9]\d{2})|(1((9[3-9])|\d{3,}))|\d{4,})"
    )


def test_integer_match():
    for start, stop in [(1, 99), (24, 89), (51, 909)]:
        for i in range(1000):
            m = (
                Regex(StartOfString(), Integer(start, stop), EndOfString())
                .compile()
                .match(str(i))
            )
            if start <= i <= stop:
                assert m is not None
            else:
                assert m is None


def test_leading_zeros():
    assert Regex(Integer(1, 12), match_start=True, match_end=True).compile().match("08")

    assert (
        Regex(Integer(1, 12, leading_zeros=False), match_start=True, match_end=True,)
        .compile()
        .match("08")
        is None
    )

    assert (
        Regex(Integer(1, 12), match_start=True, match_end=True).compile().match("089")
        is None
    )
