"""
Custom exceptions for agent_routers.

This module centralizes all library-specific errors,
making error handling predictable and explicit.
"""


class AgentRouterError(Exception):
    """Base exception for all agent_routers errors."""
    pass


class NoAgentMatchedError(AgentRouterError):
    """
    Raised when no registered agent matches the given input.

    Attributes:
        input_text (str): The input that failed routing.
    """

    def __init__(self, input_text: str):
        self.input_text = input_text
        super().__init__(f"No agent matched the input: '{input_text}'")


class AgentAlreadyRegisteredError(AgentRouterError):
    """
    Raised when trying to register an agent that already exists.

    Attributes:
        agent_name (str): The duplicate agent name.
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        super().__init__(f"Agent '{agent_name}' is already registered.")


class InvalidRuleError(AgentRouterError):
    """
    Raised when a rule definition is invalid (e.g., malformed regex).

    Attributes:
        rule (str): The invalid rule definition.
    """

    def __init__(self, rule: str):
        self.rule = rule
        super().__init__(f"Invalid rule provided: '{rule}'")
