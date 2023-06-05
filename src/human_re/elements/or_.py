from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional, Tuple, Union

from human_re.elements.multiple import Multiple, Range, _SpecialQuantifier
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.nameable import Nameable
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Or(RegexElement, Quantifiable, Nameable):
    """
    todo: doc
    Represents a Regex element that implements a logical Or: It matches any of the given patterns
    todo: name
    """

    regexes: Tuple[RegexElement, ...]
    """ Tuple[RegexElement]: The regex elements from which any can match"""

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier]
    """ The number of times the entire element should be matched (default: 1). Read `src.elements.multiple.Multiple` doc 
    for more information about the options here."""

    name: Optional[str]
    """ Name of the matching group. None is also allowed. Read `src.elements.named.Named` 
    doc for more information about the options here."""

    def __init__(
        self,
        *regexes: RegexElement,
        times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier] = 1,
        name: Optional[str] = None
    ):
        object.__setattr__(self, "regexes", regexes)
        object.__setattr__(self, "times", times)
        object.__setattr__(self, "name", name)
        if len(self.regexes) == 0:
            raise ValueError("Or must at least contain one regex element")

    def compile(self) -> Pattern:
        return Multiple(
            RegexPattern(
                re.compile(
                    "(" + "|".join(rx.compile().pattern for rx in self.regexes) + ")"
                ),
            ),
            times=self.times,
            name=self.name,
        ).compile()
