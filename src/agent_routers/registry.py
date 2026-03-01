from typing import Dict, List
from .models import Agent


class AgentRegistry:

    def __init__(self):
        self._agents: Dict[str, Agent] = {}

    def register(self, agent: Agent):
        if agent.name in self._agents:
            raise ValueError(f"Agent '{agent.name}' already registered.")
        self._agents[agent.name] = agent

    def get(self, name: str) -> Agent:
        if name not in self._agents:
            raise ValueError(f"Agent '{name}' not found.")
        return self._agents[name]

    def list_names(self) -> List[str]:
        return list(self._agents.keys())
