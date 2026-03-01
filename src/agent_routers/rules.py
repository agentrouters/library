import re
from typing import Optional, Dict


class RegexClassifier:

    def __init__(self):
        self._rules: Dict[str, str] = {}

    def add_rule(self, pattern: str, agent_name: str):
        self._rules[pattern] = agent_name

    def classify(self, text: str) -> Optional[str]:
        for pattern, agent_name in self._rules.items():
            if re.search(pattern, text, re.IGNORECASE):
                return agent_name
        return None
