from __future__ import annotations

from dataclasses import dataclass
from typing import Pattern, Tuple, Union

from human_re.elements.literal import Literal
from human_re.elements.multiple import Range, _SpecialQuantifier
from human_re.elements.or_ import Or
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class LiteralSet(RegexElement, Quantifiable):
    """
    Represents a set of literal values in a regular expression pattern.
    todo: name
    """

    literals: Tuple[str, ...]
    """A tuple of string to be matched in the regular expression pattern literal."""

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier]
    """ The number of times one of the literal should be matched (default: 1).  Read `src.elements.multiple.Multiple` 
    doc for more information about the options here."""

    def __init__(
        self,
        *literals: str,
        times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier] = 1
    ):
        object.__setattr__(self, "literals", literals)
        object.__setattr__(self, "times", times)
        if len(self.literals) == 0:
            raise ValueError("LiteralSet cannot be empty")

    def compile(self) -> Pattern:
        return Or(*(Literal(lit) for lit in self.literals), times=self.times).compile()
