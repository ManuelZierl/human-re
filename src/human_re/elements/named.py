import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional

from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Named(RegexElement):
    """
    Represents a named matching group Name can also be None than regex element is just passed.
    """

    regex: RegexElement
    """ regex (RegexElement): The regex element to that should be put in a named matching group."""

    name: Optional[str] = None
    """name of the matching group. None is also allowed."""

    def compile(self) -> Pattern:
        if self.name:
            return re.compile(f"(?P<{self.name}>{self.regex.compile().pattern})")
        return self.regex.compile()
