from __future__ import annotations

from dataclasses import dataclass
from re import Pattern

from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class RegexPattern(RegexElement):
    """
    Represents a Regex element that is directly defined by a given pattern.
    todo: test
    """

    regex: Pattern

    def compile(self) -> Pattern:
        return self.regex
