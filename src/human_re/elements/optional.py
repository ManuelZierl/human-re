from dataclasses import dataclass
from re import Pattern
from typing import Optional

from human_re.elements.multiple import Multiple, Range
from human_re.elements.regex import Regex
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Optional(RegexElement):
    """
    Represents an optional element in a regular expression pattern.
    Given Regex element is matched 0 or 1 times-
    """

    regex: RegexElement
    """A RegexElement object representing the element to be made optional."""

    name: Optional[str] = None
    """ name of the matching group. None is also allowed. Read `src.elements.named.Named` 
    doc for more information about the options here."""

    def compile(self) -> Pattern:
        return Multiple(Regex(self.regex), times=Range(0, 1), name=self.name).compile()
