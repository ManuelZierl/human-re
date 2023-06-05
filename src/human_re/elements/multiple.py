from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional, Tuple, Union

from human_re.elements.named import Named
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.nameable import Nameable
from human_re.interfaces.regex_element import RegexElement


class _SpecialQuantifier:
    pass


class SpecialQuantifier:
    LAZY: _SpecialQuantifier = _SpecialQuantifier()
    # todo: possessive matching will be introduced by python 3.11
    # POSSESSIVE: _SpecialQuantifier = _SpecialQuantifier()


@dataclass(frozen=True)
class Range:
    """
    Represents a range of repetition counts in a regular expression pattern.
    """

    start: int
    """ The starting count of repetitions."""

    stop: int
    """ The ending count of repetitions. It can also be '...' to represent an unbounded range."""

    def __post_init__(self):
        if not isinstance(self.start, int):
            raise TypeError("Range start must be int")

        if not (isinstance(self.stop, int) or self.stop is ...):
            raise TypeError("Range stop must be int or ...")

        if self.stop is not ... and not self.start <= self.stop:
            raise ValueError("Range start must be greater then stop")

    def compile_quantifier(self) -> str:
        """
        Compiles the multiple repetition element into a regular expression pattern.
        """
        if self.start == 1 and self.stop == 1:
            return ""

        if self.start == self.stop:  # but if one and 1 -> no
            return f"{{{self.start}}}"

        if self.start == 0 and self.stop == 1:
            return "?"

        if self.start == 0 and self.stop is ...:
            return "*"

        if self.start == 1 and self.stop is ...:
            return "+"

        if self.stop is ...:
            return f"{{{self.start},}}"

        return f"{{{self.start},{self.stop}}}"


@dataclass(frozen=True)
class Multiple(RegexElement, Nameable):
    """
    Represents a multiple repetition element in a regular expression pattern.
    """

    regex: RegexElement
    """ regex (RegexElement): The regex element to repeat."""

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier]
    """ The number of times the regex element should be repeated.  

        It can be one of the following types:  
          - int: The exact number of repetitions.  
          - Tuple[int, ...]: A tuple of specific repetition counts, matched in any order.  
          - Range: A range of repetition counts.  See `src.elements.multiple.Range` for more details
          - LAZY: Matches lazy: one to unlimited times but as less as possible
          - POSSESSIVE: Matches possessive: A possessive quantifier matches as many occurrences of the preceding element as possible, 
                without backtracking.
    """

    name: Optional[str] = None
    """ name of the matching group. None is also allowed. Read `src.elements.named.Named` 
    doc for more information about the options here."""

    def compile(self) -> Pattern:
        return Named(RegexPattern(self.compile_nameless()), name=self.name).compile()

    def compile_nameless(self) -> Pattern:
        if isinstance(self.times, Range):
            return re.compile(
                self.regex.compile().pattern + self.times.compile_quantifier()
            )
        if isinstance(self.times, tuple):
            return re.compile(
                "("
                + "|".join(
                    self.regex.compile().pattern + f"{{{t}}}"
                    for t in sorted(self.times, reverse=True)
                )
                + ")"
            )
        if self.times == 1:
            return self.regex.compile()
        if self.times is SpecialQuantifier.LAZY:
            return re.compile(self.regex.compile().pattern + "*?")

        return re.compile(self.regex.compile().pattern + f"{{{self.times}}}")
