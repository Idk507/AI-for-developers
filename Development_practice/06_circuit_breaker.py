"""
Understanding the problem
In Day 2, you implemented a retry decorator.

Your retry decorator attempts an operation again when it encounters temporary failures.

That works well for occasional failures.

However, consider a different situation.

You are developing an AI agent that communicates with an external LLM API.

The API becomes unavailable for ten minutes.

Your application continues receiving requests, and every request triggers three retry attempts.

If 1,000 incoming requests reach your application, the retry mechanism could generate up to 3,000 unsuccessful upstream calls.

This wastes resources, increases latency, and may place additional pressure on an already failing dependency.

A circuit breaker solves a different problem from a retry mechanism.

Instead of repeatedly attempting operations against a dependency that appears unhealthy, it temporarily blocks requests to that dependency.

The circuit breaker generally operates through three states.
State 1 — CLOSED
The service is considered available.

Requests are permitted, and the circuit breaker monitors failures.

If consecutive failures reach a configured threshold, the circuit transitions to OPEN.
State 2 — OPEN
The service is considered unavailable.

New requests are immediately rejected without invoking the underlying operation.

After a configured recovery timeout, the circuit becomes eligible for a trial request.
State 3 — HALF_OPEN
The circuit allows a limited trial request to determine whether the service has recovered.

If the trial succeeds, the circuit returns to CLOSED.

If the trial fails, the circuit returns to OPEN.

For today's exercise, assume a single-threaded implementation with one trial request in HALF_OPEN.


"""

from enum import Enum
import time 
class State(Enum):
    CLOSED = "Closed"
    OPEN = "Open"
    HALF_OPEN = "half_open"

class CircuitBreker:
    def __init__(
            self, failure_threshold : int = 3 ,
                recovery_timeout : int = 10
    ) :
        self.failure_threshold = failure_threshold 
        self.recovery_timeout = recovery_timeout 
        self.failuer_time = None 
        self.state = State.CLOSED 
        self.failure_count = 0 

    def call(
            self, func, *args, **kwargs

    ): 
        if self.state == State.OPEN :
            elapsed_time = time.time() - self.failuer_time
            if elapsed_time >=  self.recovery_timeout :
                self.state = State.HALF_OPEN 
            else : 
                raise Exception("Circuit is open")

        try :
            result = func(*args,**kwargs)
            self.failuer_count = 0   

            if self.state == State.HALF_CLOSED :
                self.state = State.CLOSED

        except : 
            self.failuer_count +=1

            self.failuer_time = time.time()

            if self.failuer_count >= self.failure_threshold or self.state == State.HALF_CLOSE :
                print("CB is open")
                self.state = State.OPEN


api_should_fail = True


def call_llm():
    global api_should_fail

    if api_should_fail:
        raise Exception("LLM API unavailable")

    return "AI response generated"


