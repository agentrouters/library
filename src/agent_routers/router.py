import inspect
from typing import List, Any, Optional

from .models import Rule
from .exceptions import (
    NoAgentMatchedError,
    AgentAlreadyRegisteredError,
)
from .engines.deterministic import DeterministicEngine
from .engines.base import BaseRoutingEngine


class AgentRouter:
    """
    Async-first agent router with pluggable routing engines.
    """

    def __init__(
        self,
        engine: Optional[BaseRoutingEngine] = None
    ) -> None:
        self._rules: List[Rule] = []
        self._registered_names = set()
        self._engine = engine or DeterministicEngine()

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
        self._rules.sort(reverse=True)

    async def route(self, input_text: str) -> Any:

        matched_rule = await self._engine.match(
            input_text,
            self._rules
        )

        if not matched_rule:
            raise NoAgentMatchedError(input_text)

        if inspect.iscoroutinefunction(matched_rule.handler):
            return await matched_rule.handler(input_text)

        return matched_rule.handler(input_text)
