import pytest

from human_re import Letter


def test_letter_validation():
    with pytest.raises(ValueError):
        Letter("ab")

    with pytest.raises(ValueError):
        Letter("a", "xy")

    with pytest.raises(ValueError):
        Letter("a", "ü")

    with pytest.raises(ValueError):
        Letter("b", "a")

    with pytest.raises(ValueError):
        Letter("A", "b")


def test_letter_compile():
    assert Letter().compile().pattern == "[A-Za-z]"
    assert Letter(umlauts=True).compile().pattern == "[A-Za-züöäÜÖÄ]"
    assert Letter(case_sensitive=True).compile().pattern == "[a-z]"
    assert Letter(stop="v", case_sensitive=True).compile().pattern == "[a-v]"
    assert Letter("a", "f", case_sensitive=True).compile().pattern == "[a-f]"
    assert (
        Letter("b", "f", case_sensitive=True, times=3).compile().pattern == "[b-f]{3}"
    )

    assert Letter("A", "X", case_sensitive=True).compile().pattern == "[A-X]"
    assert Letter("a", "f").compile().pattern == "[A-Fa-f]"

    assert (
        Letter("a", "c", umlauts=True, case_sensitive=True).compile().pattern
        == "[a-cüöä]"
    )
    assert Letter("a", "c", umlauts=True).compile().pattern == "[A-Ca-cüöäÜÖÄ]"
    assert (
        Letter("A", "C", umlauts=True).compile().pattern
        == Letter("a", "c", umlauts=True).compile().pattern
    )

    assert Letter(additional_characters=("ß", "?")).compile().pattern == "[A-Za-zß\?]"
