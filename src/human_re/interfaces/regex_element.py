from __future__ import annotations

from re import Pattern
from typing import Protocol


class RegexElement(Protocol):
    """
    Main protocol that should be implemented by all RegexElements
    """

    def compile(self) -> Pattern:
        ...
