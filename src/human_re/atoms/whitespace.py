from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional, Tuple, Union

from human_re.elements.multiple import Multiple, Range, _SpecialQuantifier
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.custom_not import CustomNot
from human_re.interfaces.nameable import Nameable
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Whitespace(RegexElement, CustomNot, Quantifiable, Nameable):
    """
    Matches any space, tab or newline character.
    """

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier] = 1
    """ The number of times whitespace should be matched (default: 1).  Read `src.elements.multiple.Multiple` 
    doc for more information about the options here."""

    name: Optional[str] = None
    """ name of the matching group. None is also allowed. Read `src.elements.named.Named` 
    doc for more information about the options here."""

    def compile(self) -> Pattern:
        return Multiple(
            RegexPattern(re.compile("\s")), times=self.times, name=self.name
        ).compile()

    def custom_not(self) -> Optional[Pattern]:
        return Multiple(
            RegexPattern(re.compile("\S")), times=self.times, name=self.name
        ).compile()
