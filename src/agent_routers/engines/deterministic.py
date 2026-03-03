import re
from typing import List, Optional
from .base import BaseRoutingEngine
from ..models import Rule


class DeterministicEngine(BaseRoutingEngine):
    """
    Default regex-based routing engine.
    """

    async def match(self, input_text: str, rules: List[Rule]) -> Optional[Rule]:
        for rule in rules:
            if rule.compiled_pattern.search(input_text):
                return rule
        return None
