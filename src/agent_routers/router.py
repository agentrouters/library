import inspect
from typing import List, Any

from .models import Rule
from .exceptions import (
    NoAgentMatchedError,
    AgentAlreadyRegisteredError,
)


class AgentRouter:
    """
    Async-first agent router with priority-based matching.
    """

    def __init__(self) -> None:
        self._rules: List[Rule] = []
        self._registered_names = set()

    def register(
        self,
        name: str,
        pattern: str,
        handler,
        priority: int = 0,
    ) -> None:

        if name in self._registered_names:
            raise AgentAlreadyRegisteredError(name)

        rule = Rule(
            priority=priority,
            name=name,
            pattern=pattern,
            handler=handler,
        )

        self._rules.append(rule)
        self._registered_names.add(name)

        # Sort once when registering (descending priority)
        self._rules.sort(reverse=True)

    async def route(self, input_text: str) -> Any:

        for rule in self._rules:
            if rule.compiled_pattern.search(input_text):

                if inspect.iscoroutinefunction(rule.handler):
                    return await rule.handler(input_text)

                return rule.handler(input_text)

        raise NoAgentMatchedError(input_text)
