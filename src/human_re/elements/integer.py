from __future__ import annotations

from dataclasses import dataclass
from re import Pattern
from typing import Optional, Tuple, Union

from human_re.elements.and_ import And
from human_re.elements.digit import Digit
from human_re.elements.literal import Literal
from human_re.elements.multiple import Range, SpecialQuantifier, _SpecialQuantifier
from human_re.elements.or_ import Or
from human_re.elements.regex import Regex
from human_re.interfaces.nameable import Nameable
from human_re.interfaces.quantifiable import Quantifiable
from human_re.interfaces.regex_element import RegexElement


@dataclass(frozen=True)
class Integer(RegexElement, Quantifiable, Nameable):
    """
    Represents a regex element for matching integer values within a specified range.
    """

    start: int
    """ The minimum value of the range. Only integers larger or equal to this number will be matched."""

    stop: int
    """ The maximum value of the range. Only integers smaller or equal to this number will be matched."""

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier] = 1
    """ The number of times the entire element should be matched (default: 1). Read `src.elements.multiple.Multiple` doc 
    for more information about the options here."""

    name: Optional[str] = None
    """ Name of the matching group. None is also allowed. Read `src.elements.named.Named` 
       doc for more information about the options here."""

    leading_zeros: bool = True
    """ Indicates whether leading zeros should be matched as well (default: True). Default is True so 
    `Regex(Integer(1, 12), match_start=True, match_end=True)` will match "08"."""

    def compile(self) -> Pattern:
        if self.leading_zeros:
            return Regex(
                Literal("0", times=SpecialQuantifier.LAZY),
                And(
                    Integer._regex_larger_than(str(self.start - 1)),
                    Integer._regex_0_to(str(self.stop)),
                    times=self.times,
                    name=self.name,
                ),
            ).compile()
        return And(
            Integer._regex_larger_than(str(self.start - 1)),
            Integer._regex_0_to(str(self.stop)),
            times=self.times,
            name=self.name,
        ).compile()

    @staticmethod
    def _regex_0_to(x: str) -> RegexElement:
        """
        Helper method to generate the regex pattern for matching integers from 0 to a given value.

        :param x: The string representation of the upper bound value.
        :return: RegexElement with regex pattern for matching integers from 0 to the specified value.
        """
        if len(x) == 1:
            return Digit(0, int(x[0]))
        elif x[0] == "0":
            return Or(
                Regex(Literal(x[0]), Integer._regex_0_to(x[1:])),
                Digit(times=Range(1, len(x) - 1)),
            )
        else:
            return Or(
                Regex(Digit(0, int(x[0]) - 1), Digit(times=Range(1, len(x) - 1))),
                Regex(Literal(x[0]), Integer._regex_0_to(x[1:])),
                Digit(times=Range(1, len(x) - 1)),
            )

    @staticmethod
    def _regex_larger_than(x: str) -> RegexElement:
        """
        Helper method to generate the regex pattern for matching integers larger than a given value.

        :param x: The string representation of the lower bound value.
        :return: RegexElement with regex pattern for matching integers larger than the specified value.
        """
        if len(x) == 1:
            return Digit(int(x[0]) + 1, 9)
        elif x[0] == "9":
            return Or(
                Regex(Literal(x[0]), Integer._regex_larger_than(x[1:])),
                Digit(times=Range(len(x) + 1, ...)),
            )
        else:
            return Or(
                Regex(Digit(int(x[0]) + 1, 9), Digit(times=len(x) - 1)),
                Regex(Literal(x[0]), Integer._regex_larger_than(x[1:])),
                Digit(times=Range(len(x) + 1, ...)),
            )
