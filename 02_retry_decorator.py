"""
Part 2 — Software Engineering: Build a Retry Decorator
Difficulty: Beginner → Intermediate | Time: 45–60 minutes
This is today's main engineering challenge.
Understanding the problem
Imagine you're developing an AI agent that calls an external API to retrieve information.
Occasionally, the API fails because of temporary network interruptions or service unavailability.
Should the application immediately terminate?
Not necessarily. For transient failures, retrying the operation can improve reliability.
For example, suppose an API request fails twice but succeeds on its third attempt.
Attempt 1 → TimeoutError
Attempt 2 → TimeoutError
Attempt 3 → Success

Final result → Success

Instead of implementing retry logic separately for every API function, we can create a reusable Python decorator.
A decorator wraps another function and adds behavior without modifying that function's implementation.
Required behavior
Create a decorator named retry.
It should accept a maximum number of attempts, a delay between attempts, and the exception types that are eligible for retrying.
Use the following interface:

"""

# Attempt : 1

import time
from collections.abc import Callable
from functools import wrap

def retry(
    max_attempts: int = 3,
    delay_seconds: float = 0.0,
    exceptions: tuple[type[Exception], ...] = (
        TimeoutError,
        ConnectionError,
    ),
    sleep: Callable[[float], None] = time.sleep,
) -> Callable:
    """
    Return a decorator that retries a synchronous function
    when it raises one of the configured exceptions.

    Retry at most max_attempts times, including the
    initial invocation.

    Raise the final exception if all attempts fail.
    """
    
    def decorator(func):
        @wrap(func)
        def wrapper(*args,**kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e :
                    if attempt < max_attempts -1:
                        sleep(delay_seconds)
                    else:
                        raise e
        return wrapper 
    return decorator            




@retry(max_attempts=3, delay_seconds=2, exceptions=(TimeoutError,))
def fetch_data():
    print("Trying to fetch data...")
    raise TimeoutError("Network issue!")  # simulate failure

fetch_data()


#correct solution 

import math
import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int = 3,
    delay_seconds: float = 0.0,
    exceptions: tuple[type[Exception], ...] = (
        TimeoutError,
        ConnectionError,
    ),
    sleep: Callable[[float], None] = time.sleep,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry synchronous operations for configured transient exceptions."""

    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int):
        raise TypeError("max_attempts must be an integer")

    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")

    if (
        isinstance(delay_seconds, bool)
        or not isinstance(delay_seconds, (int, float))
    ):
        raise TypeError("delay_seconds must be numeric")

    if not math.isfinite(delay_seconds) or delay_seconds < 0:
        raise ValueError("delay_seconds must be finite and nonnegative")

    if (
        not isinstance(exceptions, tuple)
        or not exceptions
        or not all(
            isinstance(exc, type) and issubclass(exc, Exception)
            for exc in exceptions
        )
    ):
        raise TypeError("exceptions must be a nonempty tuple of exception classes")

    if not callable(sleep):
        raise TypeError("sleep must be callable")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        """Wrap a function with bounded retry behavior."""

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Run the function and retry eligible failures."""
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:
                        raise

                    sleep(delay_seconds)

            # Unreachable with valid max_attempts, but explicit for clarity.
            raise RuntimeError("Retry loop terminated unexpectedly")

        return wrapper

    return decorator