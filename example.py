import asyncio
from agent_routers import AgentRouter
from agent_routers.exceptions import NoAgentMatchedError


async def main():

    router = AgentRouter()

    # ----------------------------
    # Sync handler
    # ----------------------------
    def greet_handler(text: str):
        return "Hi %s great? (sync)" % text

    # ----------------------------
    # Async handler
    # ----------------------------
    async def support_handler(text: str):
        return "The support handler was called (async) with input:  %s" % text

    # ----------------------------
    # Register rules
    # ----------------------------
    router.register(
        name="greet",
        pattern=r"\bhello\b|\bhi\b",
        handler=greet_handler,
        priority=1,
    )

    router.register(
        name="support",
        pattern=r"error|bug",
        handler=support_handler,
        priority=10,
    )

    # ----------------------------
    # Test 1 - Async handler (higher priority)
    # ----------------------------
    result1 = await router.route("Go to error route!")
    print("Test 1:", result1)

    # ----------------------------
    # Test 2 - Sync handler
    # ----------------------------
    result2 = await router.route("hello world")
    print("Test 2:", result2)

    # ----------------------------
    # Test 3 - Priority check
    # ----------------------------
    router.register(
        name="low_priority",
        pattern=r"hello world",
        handler=lambda x: "LOW PRIORITY",
        priority=0,
    )

    result3 = await router.route("hello world")
    print("Test 3:", result3)

    # ----------------------------
    # Test 4 - No match
    # ----------------------------
    try:
        await router.route("something unknown happened")
    except NoAgentMatchedError as e:
        print("Test 4: Exception caught ->", e)


if __name__ == "__main__":
    asyncio.run(main())
