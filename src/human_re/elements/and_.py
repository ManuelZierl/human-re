from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional, Tuple, Union

from human_re.elements.multiple import Range, _SpecialQuantifier
from human_re.elements.regex import Regex
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.nameable import Nameable
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class And(RegexElement, Nameable, Quantifiable):
    """
    Represents a Regex element that functions as a logical And. The Regex must match
    all given patterns to be matched. This is achieved by applying a positive lookahead
    (non-consuming) to all but the last pattern.
    """

    regexes: Tuple[RegexElement, ...]
    """ Tuple[RegexElement]: The regex elements to that must all match"""

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
        name: Optional[str] = None,
    ):
        object.__setattr__(self, "regexes", regexes)
        object.__setattr__(self, "times", times)
        object.__setattr__(self, "name", name)
        if len(self.regexes) == 0:
            raise ValueError("And must at least contain one regex element")

    def compile(self) -> Pattern:
        return Regex(
            *(
                RegexPattern(re.compile(f"(?={regex.compile().pattern})"))
                for regex in self.regexes[:-1]
            ),
            self.regexes[-1],
            times=self.times,
            name=self.name,
        ).compile()
