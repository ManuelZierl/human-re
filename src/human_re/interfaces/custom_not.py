from re import Pattern
from typing import Optional, Protocol, runtime_checkable


@runtime_checkable
class CustomNot(Protocol):
    """
    This protocol can be used by `RegexElements` that want to implement a custom negation behavior when used with
    the `src.elements._not.Not`. Implementing this protocol allows the element to define a custom
    behavior for negation.
    The `custom_not` method defined by this protocol can return either `None`, in which case the default negation
    behavior is used, or a pattern that will be used instead of the default behavior.
    """

    def custom_not(self) -> Optional[Pattern]:
        ...
