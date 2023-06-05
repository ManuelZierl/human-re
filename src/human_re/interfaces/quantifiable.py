from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Tuple, Union

if TYPE_CHECKING:
    from human_re.elements.multiple import _SpecialQuantifier, Range


class Quantifiable(Protocol):
    """
    This protocol can be used by RegexElements to indicate that the given element is quantifiable. For more information
    about the options read the doc of `src.element.multiple.Multiple`
    """

    times: Union[int, Tuple[int, ...], Range, _SpecialQuantifier]
