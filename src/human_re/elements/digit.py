from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional, Tuple, Union

import human_re.utils as utils
from human_re.elements.multiple import Multiple, Range, _SpecialQuantifier
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.custom_not import CustomNot
from human_re.interfaces.nameable import Nameable
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Digit(RegexElement, CustomNot, Nameable, Quantifiable):
    """
    Represents a digit element in a regular expression pattern.
    """

    start: int = 0
    """The starting digit (default: 0). Must be between 0 and 9 (inclusive)"""

    stop: int = 9
    """The ending digit (default: 9).  Must be between 0 and 9 (inclusive)"""

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier] = 1
    """The number of times the digit element should be matched (default: 1). Read `src.elements.multiple.Multiple` doc 
    for more information about the options here."""

    name: Optional[str] = None
    """ name of the matching group. None is also allowed. Read `src.elements.named.Named` 
    doc for more information about the options here."""

    def compile(self) -> Pattern:
        """
        Compiles the digit element into a regular expression pattern.
        """
        if self.start == self.stop:
            return Multiple(
                RegexPattern(re.compile(str(self.start))),
                times=self.times,
                name=self.name,
            ).compile()
        if self.start == 0 and self.stop == 9:
            return Multiple(
                RegexPattern(re.compile("\d")), times=self.times, name=self.name
            ).compile()
        return Multiple(
            RegexPattern(re.compile(f"[{self.start}-{self.stop}]")),
            times=self.times,
            name=self.name,
        ).compile()

    def custom_not(self) -> Optional[Pattern]:
        if self.start == 0 and self.stop == 9:
            return Multiple(
                RegexPattern(re.compile("\D")), times=self.times, name=self.name
            ).compile()

    def __post_init__(self):
        if not utils.int_is_digit(self.start):
            raise ValueError("Digit.start must be between 0 and 9")
        if not utils.int_is_digit(self.stop):
            raise ValueError("Digit.stop must be between 0 and 9")
        if self.start > self.stop:
            raise ValueError("Digit.start cannot be larger than Digit.stop")
