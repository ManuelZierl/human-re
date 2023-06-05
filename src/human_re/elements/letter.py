from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import Tuple, Union, Optional

import human_re.utils as utils
from human_re.elements.multiple import Multiple, Range, _SpecialQuantifier
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Letter(RegexElement, Quantifiable):
    """
    Represents a letter element in a regular expression pattern.
    """

    start: str = "a"
    """ The starting letter (default: 'a'). Must be between 'a' and 'z' (inclusive)."""

    stop: str = "z"
    """ The ending letter (default: 'z'). Must be between 'a' and 'z' (inclusive)."""

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier] = 1
    """ The number of times the letter element should be matched (default: 1).  Read `src.elements.multiple.Multiple` 
    doc for more information about the options here."""

    case_sensitive: bool = False
    """ Flag indicating if the letter matching should be case-sensitive (default: False)"""

    umlauts: bool = False
    """ Flag indicating if umlaut characters (üöä) should be included (default: False)"""

    additional_characters: Tuple[str, ...] = tuple()
    """ Additional characters to include in the letter matching (default: empty tuple)."""

    name: Optional[str] = None
    """ name of the matching group. None is also allowed. Read `src.elements.named.Named` 
    doc for more information about the options here."""

    def compile(self) -> Pattern:
        letter_pattern_str = f"{self.start}-{self.stop}"
        if self.umlauts:
            letter_pattern_str += "üöä" if self.start.islower() else "ÜÖÄ"

        if not self.case_sensitive:
            letter_pattern_str = f"{self.start.upper()}-{self.stop.upper()}{self.start.lower()}-{self.stop.lower()}"
            if self.umlauts:
                letter_pattern_str += "üöäÜÖÄ"

        letter_pattern_str += "".join(
            re.escape(char) for char in self.additional_characters
        )
        letter_pattern_str = f"[{letter_pattern_str}]"

        return Multiple(
            RegexPattern(re.compile(letter_pattern_str)), times=self.times, name=self.name
        ).compile()

    def __post_init__(self):
        if not utils.str_is_char(self.start) or not utils.char_is_a_to_z(self.start):
            raise ValueError("Letter.start must be between a and z")
        if not utils.str_is_char(self.stop) or not utils.char_is_a_to_z(self.stop):
            raise ValueError("Letter.stop must be between a and z")
        if self.start > self.stop:
            raise ValueError("Letter.start cannot be larger than Letter.stop")
        if self.additional_characters:
            if any(not utils.str_is_char(char) for char in self.additional_characters):
                raise ValueError("Additional characters must be single characters")
        if not (
            (self.start.isupper() and self.stop.isupper())
            or (self.start.islower() and self.stop.islower())
        ):
            raise ValueError(
                "Letter.start and Letter.stop must have same case. Either both upper or both lower."
            )
