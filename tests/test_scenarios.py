import re

from human_re import (
    Digit,
    Integer,
    Letter,
    Literal,
    LiteralSet,
    Optional,
    Or,
    Range,
    Regex,
    Whitespace,
)


def test_hex_color_regex():
    # this is just a test example, so no guarantee for correctness
    hex_color_regex = Regex(Literal("#"), Or(Digit(), Letter("a", "f"), times=(3, 6)))

    assert hex_color_regex.compile().match("#fff")
    assert hex_color_regex.compile().match("#1ed99e")
    assert hex_color_regex.compile().match("#1eg99e") is None


def test_email_regex():
    # this is just a test example, so no guarantee for correctness
    email_regex = Regex(
        Letter(additional_characters=(".", "_", "%", "+", "-"), times=Range(1, ...)),
        Literal("@"),
        Letter(additional_characters=(".", "_", "%", "+", "-"), times=Range(1, ...)),
        Literal("."),
        Letter(times=Range(2, ...)),
    )
    # ([A-Za-z\\._%\\+\\-]+@[A-Za-z\\._%\\+\\-]+\\.[A-Za-z]{2,})

    assert email_regex.compile().match("max.musterman@mail.de")
    assert email_regex.compile().match("@mail.de") is None
    assert email_regex.compile().match("max.mustermann@mail") is None


def test_url_regex():
    # this is just a test example, so no guarantee for correctness
    url_regex = Regex(
        Literal("http"),
        Optional(Literal("s")),
        Literal("://"),
        Optional(Literal("www.")),
        Or(
            Letter(),
            Digit(),
            LiteralSet("-", "@", ":", "%", ".", "_", "+", "~", "#", "="),
            times=Range(1, 256),
        ),
        Literal("."),
        Or(Letter(), Digit(), LiteralSet("(", ")"), times=Range(1, 6)),
        Or(
            Letter(),
            Digit(),
            LiteralSet(
                "-",
                "(",
                ")",
                "@",
                ":",
                "%",
                "_",
                "\\",
                "+",
                ".",
                "~",
                "#",
                "?",
                "&",
                "/",
                "=",
            ),
            times=Range(0, ...),
        ),
        match_start=True,
        match_end=True,
    ).compile()

    for url in [
        "https://www.example.com",
        "http://subdomain.example.com",
        "https://www.example.com/path/to/page.html",
        "http://www.example.com?param1=value1&param2=value2",
        "https://www.example.com#section",
        "https://www.example.co.uk",
        "https://www.example.com:8443",
    ]:
        assert url_regex.match(url)

    for no_url in [
        "www.example.com",  # Missing protocol
        "example.com",  # Missing protocol and www
        "http:/www.example.com",  # Incorrect protocol delimiter
        "http//www.example.com",  # Missing colon after protocol
        "http://www.ex ample.com",  # Space within the URL
        "http://www.example.com/path/with spaces",  # Space within the path
    ]:
        assert url_regex.match(no_url) is None


def test_basic_date_regex():
    date_regex = Regex(
        Digit(times=4, name="year"),
        Literal("-"),
        Integer(1, 12, name="month"),
        Literal("-"),
        Integer(1, 31, name="day"),
        match_start=True,
        match_end=True,
    ).compile()

    assert date_regex.match("2031-12-24")
    assert date_regex.match("2031-12-32") is None


def test_german_license_plate():
    german_plate_regex = Regex(
        Letter(
            "A",
            "Z",
            case_sensitive=True,
            umlauts=True,
            times=Range(1, 3),
            name="region",
        ),
        Literal("-"),
        Letter("A", "Z", case_sensitive=True, times=Range(1, 2)),
        Optional(Whitespace()),
        Digit(1, 9),
        Digit(0, 9, times=Range(0, 3)),
        Optional(
            Regex(
                Optional(Whitespace()),
                Or(
                    Literal("E", name="is_electric_car"),
                    Literal("H", name="is_antique_car"),
                ),
            ),
        ),
        match_start=True,
        match_end=True
    ).compile()
    # '^((?P<region>[A-ZÜÖÄ]{1,3})\\-[A-Z]{1,2}(\\s)?[1-9]\\d{0,3}(((\\s)?((?P<is_electric_car>E)|(?P<is_antique_car>H))))?)$'

    assert german_plate_regex.match("DEG-QB1")
    assert german_plate_regex.match("HH-W1000")

    assert german_plate_regex.match("DEG-QB01") is None
    assert german_plate_regex.match("HH-WXXX 1000") is None

    assert german_plate_regex.match("M-AB 123").group("region") == "M"
    assert german_plate_regex.match("M-AB 123 E").group("is_electric_car") == "E"
    assert german_plate_regex.match("M-AB 123H").group("is_antique_car") == "H"

