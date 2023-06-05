from typing import Optional, Protocol


class Nameable(Protocol):
    """
    This protocol can be used by `RegexElements` to indicate that the element can be named and included in a named
    matching group using the provided name.
    """

    name: Optional[str]
