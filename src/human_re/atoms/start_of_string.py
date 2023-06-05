import re
from dataclasses import dataclass
from re import Pattern

from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class StartOfString(RegexElement):
    """
    Matches the start of a string without consuming any characters.
    """

    def compile(self) -> Pattern:
        return re.compile("^")
