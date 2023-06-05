import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional

from human_re.interfaces.custom_not import CustomNot
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Boundary(RegexElement, CustomNot):
    """
    Represents a regex element that matches the boundary of a word without consuming any characters.
    """

    def compile(self) -> Pattern:
        return re.compile("\b")

    def custom_not(self) -> Optional[Pattern]:
        return re.compile("\B")
