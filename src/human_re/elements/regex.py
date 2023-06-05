from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Pattern, Tuple, Union

from human_re.elements.multiple import Multiple, Range, _SpecialQuantifier
from human_re.elements.named import Named
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.nameable import Nameable
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Regex(RegexElement, Quantifiable, Nameable):
    """
    Regex element that serves as a wrapper around multiple given regex elements that are concatenated sequentially
    """

    regexes: Tuple[RegexElement, ...]
    """ Tuple[RegexElement]: The regex elements that should be applied sequentially"""

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier]
    """ The number of times the entire element should be matched (default: 1). Read `src.elements.multiple.Multiple` doc 
    for more information about the options here."""

    name: Optional[str]
    """ Name of the matching group. None is also allowed. Read `src.elements.named.Named` 
       doc for more information about the options here."""

    match_start: bool = False
    """boolean saying if start of string should be matched (default False)"""

    match_end: bool = False
    """boolean saying if end of string should be matched (default False)"""

    def __init__(
        self,
        *regexes: RegexElement,
        times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier] = 1,
        name: Optional[str] = None,
        match_start: bool = False,
        match_end: bool = False,
    ):
        object.__setattr__(self, "regexes", regexes)
        object.__setattr__(self, "times", times)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "match_start", match_start)
        object.__setattr__(self, "match_end", match_end)
        if len(self.regexes) == 0:
            raise ValueError("Regex must at least contain one regex element")

    def compile(self) -> Pattern:
        pattern = ""
        if self.match_start:
            pattern += "^"
        pattern += "(" + "".join(rx.compile().pattern for rx in self.regexes) + ")"
        if self.match_end:
            pattern += "$"

        return Named(
            Multiple(RegexPattern(re.compile(pattern)), times=self.times,),
            name=self.name,
        ).compile()
