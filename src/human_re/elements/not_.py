import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional

from human_re.elements.anything import Anything
from human_re.elements.multiple import Range
from human_re.elements.regex import Regex
from human_re.elements.regex_pattern import RegexPattern
from human_re.interfaces.custom_not import CustomNot
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Not(RegexElement, CustomNot):
    """
    Represent Regex element that matches everything but the given regex element. It does so
    by applying a negative lookahead before a anything match.
    """

    regex: RegexElement
    """the regex element that should not match."""

    def compile(self) -> Pattern:
        if isinstance(self.regex, CustomNot):
            cn = self.regex.custom_not()
            if cn is not None:
                return cn

        return Regex(
            RegexPattern(re.compile(f"(?!{self.regex.compile().pattern})")),
            Anything(times=Range(0, ...)),
        ).compile()

    def custom_not(self) -> Optional[Pattern]:
        return self.regex.compile()
