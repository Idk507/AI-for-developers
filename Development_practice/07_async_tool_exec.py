""""
Understanding the problem
Imagine you're building an AI agent using LangGraph or another orchestration framework.

The agent needs to execute three independent tools:
User Request
     |
     v
   AI Agent
     |
     +---- Document Search Tool
     |
     +---- Customer Database Tool
     |
     +---- Product Information Tool
     |
     v
Aggregate Tool Results
     |
     v
Generate Final Response

Suppose the tools take two, three, and four seconds respectively.

If executed sequentially, the total execution time would be approximately nine seconds.

However, because the tools are independent, they could execute concurrently.

In an ideal scenario with sufficient capacity, total execution time would approach four seconds rather than nine.

This introduces asynchronous programming.

Python's asyncio library allows multiple I/O-bound operations to make progress concurrently without requiring a separate operating-system thread for every operation.

For example, while one tool waits for an HTTP response, another tool can continue executing.
Your assignment
Build an asynchronous executor that runs independent tool calls concurrently while enforcing a maximum concurrency limit.

Use this interface:
from collections.abc import Awaitable, Callable, Sequenceasync def execute_tools(    tools: Sequence[Callable[[], Awaitable[str]]],    max_concurrency: int = 3,    timeout_seconds: float = 5.0,) -> list[str | Exception]:    """    Execute independent asynchronous tool operations.    Requirements:        Execute each tool exactly once.        Limit simultaneously executing tools.        Apply a timeout to each tool.        Preserve the original tool ordering.        Return exceptions as results for failed tools.        Propagate cancellation of the overall executor.    Args:        tools: Zero-argument asynchronous tool factories.        max_concurrency: Maximum number of active tool calls.        timeout_seconds: Per-tool execution timeout.    Returns:        Results or exception objects in input order.    """    pass


Expected behavior
Consider these three asynchronous operations:
import asyncioasync def search_documents() -> str:    """Simulate retrieving enterprise documents."""    await asyncio.sleep(2)    return "Documents retrieved"async def fetch_customer() -> str:    """Simulate retrieving customer information."""    await asyncio.sleep(1)    return "Customer retrieved"async def fetch_products() -> str:    """Simulate retrieving product information."""    await asyncio.sleep(3)    return "Products retrieved"


Your executor should support:
async def main() -> None:    """Run independent tools with bounded concurrency."""    results = await execute_tools(        tools=[            search_documents,            fetch_customer,            fetch_products,        ],        max_concurrency=3,        timeout_seconds=5.0,    )    print(results)if __name__ == "__main__":    asyncio.run(main())


The expected result is:
[    "Documents retrieved",    "Customer retrieved",    "Products retrieved",]


Although fetch_customer() completes before search_documents(), the returned results must preserve the original tool order.
Implementation guidance
Start by understanding three Python concepts: async def, await, and asyncio.Semaphore.

An asynchronous function declared using async def returns a coroutine object when called. The coroutine does not execute to completion merely because you created it.

The await expression allows a coroutine to suspend while another asynchronous operation progresses.

An asyncio.Semaphore controls how many operations can enter a protected section concurrently.

For example, a semaphore configured with a capacity of three permits at most three operations to hold its permits simultaneously.

Your implementation should acquire a permit before invoking a tool and release it when execution finishes, including when the tool fails.

Use asyncio.wait_for() or an equivalent timeout mechanism to enforce the per-tool execution deadline.

For this exercise, the timeout begins when the tool acquires a concurrency permit. Time spent waiting for a permit does not count toward the per-tool timeout.
Required behavior and tests
Scenario	Expected behavior
Three tools, concurrency three	Execute concurrently
Three tools, concurrency one	Execute sequentially
One tool raises ValueError	Capture exception; other tools continue
One tool exceeds its timeout	Return a timeout exception for that tool
Tools finish out of order	Preserve input ordering
Empty tool collection	Return an empty list
Invalid concurrency	Raise ValueError or TypeError
Invalid timeout	Reject nonpositive or non-finite values
Overall execution cancelled	Propagate cancellation and clean up child tasks


Boolean configuration values must not be accepted as integers or floating-point numbers.

Use pytest with pytest-asyncio for asynchronous tests.


"""