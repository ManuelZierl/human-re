from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import Tuple, Union

from human_re.elements.multiple import Multiple, Range, _SpecialQuantifier
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Literal(RegexElement, Quantifiable):
    """
    Represents a literal element in a regular expression pattern.
    todo: name
    """

    literal: str
    """The literal string to match."""

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier] = 1
    """ The number of times the letter element should be matched (default: 1).  Read `src.elements.multiple.Multiple` 
    doc for more information about the options here."""

    def compile(self) -> Pattern:
        """
        Compiles the literal element into a regular expression pattern.
        """
        return Multiple(
            RegexPattern(re.compile(re.escape(self.literal))), times=self.times
        ).compile()

    def __post_init__(self):
        if self.literal == "":
            raise ValueError("Literal cannot be empty str")
