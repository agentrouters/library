from dataclasses import dataclass, field
from typing import Callable, Awaitable, Union, Any
import re


Handler = Union[
    Callable[[str], Any],
    Callable[[str], Awaitable[Any]],
]


@dataclass(order=True)
class Rule:
    """
    Represents a routing rule.

    Rules are ordered by priority (descending).
    """
    priority: int
    name: str = field(compare=False)
    pattern: str = field(compare=False)
    handler: Handler = field(compare=False)
    compiled_pattern: re.Pattern = field(init=False, compare=False)

    def __post_init__(self):
        self.compiled_pattern = re.compile(self.pattern)
