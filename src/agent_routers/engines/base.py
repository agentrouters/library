from typing import List, Optional
from ..models import Rule


class BaseRoutingEngine:
    """
    Base interface for routing engines.
    """

    async def match(self, input_text: str, rules: List[Rule]) -> Optional[Rule]:
        """
        Return the matched Rule or None.
        """
        raise NotImplementedError
