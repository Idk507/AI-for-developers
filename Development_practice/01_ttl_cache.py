"""

Problem statement
Build an in-memory cache that stores key-value pairs with expiration times.
A Time-to-Live (TTL) cache is useful in AI applications because repeatedly fetching the same configuration, metadata, or reusable computation can increase latency and infrastructure costs.
For example, an AI agent might cache a tool's metadata for 60 seconds. Once that time expires, the cached entry must no longer be returned.

Required functionality
Your cache must support inserting a value with an expiration duration, retrieving a non-expired value, deleting an entry, and removing expired entries.
Implement this interface:

"""

import time
from collections.abc import Callable # Callable is an abstract base class for callable objects in Python, which includes functions, methods, and classes that implement the __call__ method.

class TTLCache:
    def __init__(self ,
                 clock : Callable[[], float] | None = None):
        self._clock = clock or time.monotonic 
        self._cache = {}  # dict[str, tuple[object, float]]: A dictionary to store the cached values and their expiration times.

    def set(self,
            key : str,
            value : object,
            ttl_seconds : float) -> None:
        expiration_time = self._clock() + ttl_seconds
        self._cache[key] = (value, expiration_time)


    def get(self, key : str, default : object = None) -> object:
        entry = self._cache.get(key)
        if entry is None :
            return default
        
        value , expiration_time = entry
        # compare current time with expirea at 

        if self._clock() >= expiration_time:
            del self._cache[key]
            return default

        return value

    def delete(self,key : str) -> bool:
        entry = self._cache.get(key)
        if key not in self._cache :
            return False 
        del self._cache[key]
        return True

    def purge_expired(self) -> int:

        expired_keys = []

        now = self._clock
        expired = [k for k ,(_, exp) in self._cache.items() if now >= exp]
        for k in expired:
            del self._cache[k]
            expired_keys.append(k)
        return len(expired_keys)

  

class FakeClock:
    """Provide manually controlled time for tests."""

    def __init__(self) -> None:
        self.now = 100.0

    def __call__(self) -> float:
        """Return the simulated current timestamp."""
        return self.now

    def advance(self, seconds: float) -> None:
        """Advance simulated time by a nonnegative duration."""
        if seconds < 0:
            raise ValueError("Cannot move simulated time backward.")
        self.now += seconds




clock = FakeClock()
cache = TTLCache(clock=clock)

cache.set("name", "Alice", 10)

assert cache.get("name") == "Alice"

clock.advance(9)

assert cache.get("name") == "Alice"

clock.advance(1)

assert cache.get("name") is None