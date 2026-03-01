import pytest
from agent_routers import AgentRouter
from agent_routers.exceptions import (
    NoAgentMatchedError,
    AgentAlreadyRegisteredError,
)


# ---------------------------
# Async Handler
# ---------------------------

@pytest.mark.asyncio
async def test_async_handler_routing():

    async def support_handler(text: str):
        return "support called"

    router = AgentRouter()
    router.register("support", r"error|bug", support_handler)

    result = await router.route("There is an error")

    assert result == "support called"


# ---------------------------
# Sync Handler
# ---------------------------

@pytest.mark.asyncio
async def test_sync_handler_routing():

    def greet_handler(text: str):
        return "hello"

    router = AgentRouter()
    router.register("greet", r"hello|hi", greet_handler)

    result = await router.route("hello world")

    assert result == "hello"


# ---------------------------
# No Match
# ---------------------------

@pytest.mark.asyncio
async def test_no_agent_matched():

    router = AgentRouter()

    with pytest.raises(NoAgentMatchedError):
        await router.route("nothing matches this")


# ---------------------------
# Duplicate Agent Registration
# ---------------------------

def test_duplicate_agent_registration():

    def handler(text: str):
        return "x"

    router = AgentRouter()
    router.register("agent1", r"test", handler)

    with pytest.raises(AgentAlreadyRegisteredError):
        router.register("agent1", r"other", handler)


# ---------------------------
# Same Priority → First Registered Wins
# ---------------------------

@pytest.mark.asyncio
async def test_same_priority_first_registered_wins():

    def handler1(text: str):
        return "first"

    def handler2(text: str):
        return "second"

    router = AgentRouter()

    # Same priority (default 0)
    router.register("agent1", r"hello", handler1)
    router.register("agent2", r"hello world", handler2)

    result = await router.route("hello world")

    # Same priority → insertion order preserved
    assert result == "first"


# ---------------------------
# Higher Priority Wins
# ---------------------------

@pytest.mark.asyncio
async def test_higher_priority_wins():

    def low_priority(text: str):
        return "low"

    def high_priority(text: str):
        return "high"

    router = AgentRouter()

    router.register("low", r"hello", low_priority, priority=1)
    router.register("high", r"hello world", high_priority, priority=10)

    result = await router.route("hello world")

    assert result == "high"


# ---------------------------
# Multiple Agents Different Patterns
# ---------------------------

@pytest.mark.asyncio
async def test_multiple_agents():

    def support_handler(text: str):
        return "support"

    def sales_handler(text: str):
        return "sales"

    router = AgentRouter()

    router.register("support", r"error|bug", support_handler)
    router.register("sales", r"price|buy", sales_handler)

    result_support = await router.route("There is a bug")
    result_sales = await router.route("I want to buy")

    assert result_support == "support"
    assert result_sales == "sales"


# ---------------------------
# Regex Behavior
# ---------------------------

@pytest.mark.asyncio
async def test_regex_matching():

    def handler(text: str):
        return "matched"

    router = AgentRouter()
    router.register("test", r"\d+", handler)

    result = await router.route("Order 1234")

    assert result == "matched"
