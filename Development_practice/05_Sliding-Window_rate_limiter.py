""""

Understanding the problem
Imagine you're developing a FastAPI application that exposes an LLM-powered chatbot.

Your application receives requests from thousands of users. Each request might trigger model inference, vector database retrieval, and external tool calls.

Now imagine one user sends 10,000 requests within a few seconds.

Without controls, that user could consume excessive compute capacity, increase operating costs, and degrade service for everyone else.

A rate limiter controls how frequently a client can perform an operation.

For example, suppose your application allows three requests per 10-second window.
Client: user_101

Time = 0 seconds

Request 1 → ALLOWED
Request 2 → ALLOWED
Request 3 → ALLOWED
Request 4 → BLOCKED

After enough time passes, older requests leave the window, allowing new requests.

A sliding-window rate limiter continuously evaluates recent request history rather than resetting all counters at fixed clock boundaries.
Your implementation requirements
Implement a Python class that tracks requests separately for each client.
import timefrom collections.abc import Callableclass SlidingWindowRateLimiter:    \"""Limit requests using a sliding time window.\"""    def __init__(        self,        max_requests: int,        window_seconds: float,        clock: Callable[[], float] | None = None,    ) -> None:        \"""        Initialize the rate limiter.        max_requests:            Maximum accepted requests within one window.        window_seconds:            Duration of the sliding window.        clock:            Optional monotonic clock for deterministic testing.        \"""        pass    def allow(self, client_id: str) -> bool:       \"""        Determine whether a client may make another request.        Return True and record the request if permitted.        Return False without recording it if the        request limit has been reached.       \"""        pass


Expected behavior
limiter = SlidingWindowRateLimiter(    max_requests=3,    window_seconds=10,)assert limiter.allow("user_101") is Trueassert limiter.allow("user_101") is Trueassert limiter.allow("user_101") is Trueassert limiter.allow("user_101") is False# Different clients have independent limits.assert limiter.allow("user_102") is True


Important implementation hint
Think about storing the timestamps of accepted requests for each user.

For example:
{    "user_101": [100.0, 102.0, 105.0],    "user_102": [104.0]}


Suppose the current time is 111 seconds and the window duration is 10 seconds.

The active window is:
(101, 111]

The request at timestamp 100 is no longer counted.

The requests at 102 and 105 are still counted.

Therefore, the user can make another request.

For this exercise, use the convention that a timestamp expires when:
timestamp <= current_time - window_seconds


You may explore collections.deque, which supports efficient removal from the beginning of a sequence.

However, design the logic yourself before searching for an implementation
"""

from collections import deque
import time 
from collections import Callable 

class SlidingWindow:
    def __init__(self, max_request : int ,window_size : int ,clock : Callable[[],float]):
        self.max_request = max_request
        self.window_size = window_size 
        self.clock = clock or time.monotonic
        self.history : dict[str,deque[float]] = {}

    def limit(self, client_id : str) -> bool : 
        if self.client_id not in history : 
            self.history[self.client_id] = deque()
        now =  self.clock()

        q = self.history[self.client_id]

        if len(q) >= self.max_request :
            return False

        while q and q[0] <= now - self.max_request:
            q.popleft()

        if len(q)<self.max_request :
            q.append(now)
            return True
        else: 
            return False 