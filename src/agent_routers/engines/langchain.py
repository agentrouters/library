from typing import List, Optional
from .base import BaseRoutingEngine
from ..models import Rule


class LangChainEngine(BaseRoutingEngine):
    """
    Routing engine that delegates classification to a LangChain chain.
    """

    def __init__(self, chain):
        self.chain = chain

    async def match(self, input_text: str, rules: List[Rule]) -> Optional[Rule]:

        # O chain deve retornar o nome do agente
        result = await self.chain.ainvoke({"query": input_text})

        agent_name = result.get("agent")

        for rule in rules:
            if rule.name == agent_name:
                return rule

        return None
