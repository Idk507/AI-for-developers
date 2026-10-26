"""
Understanding the problem
LRU stands for Least Recently Used.

Imagine you're building an AI application that caches recently retrieved documents.

Your cache has a maximum capacity of three entries.

Initially, you insert three documents:
Cache capacity = 3

Insert A
Insert B
Insert C

Cache = [A, B, C]

Now a user accesses document A.

Document A becomes the most recently used entry.
Cache = [B, C, A]

Next, the application needs to insert document D.

Since the cache is full, it must remove the least recently used entry, B.
Cache = [C, A, D]

This is the central idea of LRU caching.

Unlike your previous TTL cache, which removes entries based on expiration time, an LRU cache removes entries based on how recently they were accessed.
Your implementation requirements
Implement the following class:
class LRUCache:    \"""A fixed-capacity least-recently-used cache \"""    def __init__(self, capacity: int) -> None:        """        Initialize a cache with a positive maximum capacity.        Raise ValueError for nonpositive capacity.        """        pass    def get(        self,        key: str,        default: object = None,    ) -> object:        """        Return a cached value or the default.        Accessing an existing key marks it as recently used.        """        pass    def put(self, key: str, value: object) -> None:        """        Insert or update a cache entry.        If the cache exceeds capacity, evict the        least recently used entry.        """        pass    def __len__(self) -> int:        """Return the number of entries currently stored."""        pass


Expected behavior
cache = LRUCache(capacity=2)cache.put("A", 100)cache.put("B", 200)assert cache.get("A") == 100cache.put("C", 300)assert cache.get("B") is Noneassert cache.get("A") == 100assert cache.get("C") == 300assert len(cache) == 2


Notice that accessing A made it recently used. Therefore, inserting C evicted B.

Your implementation must also handle updating an existing key, accessing missing keys, storing None as a valid value, and rejecting invalid capacities.

"""

from collections import OrderedDict 

class LRUCache:
    def __init__(
            self, capacity :int 
    ):
        if capacity <= 0 :
            raise ValueError("Capcity is not supposed to be 0")
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(
            self, key : str, default : object = None
    ) :
        if key in self.cache : 
            self.cache.move_to_end(key)
            return self.cache[key]
        return default

    def put(
            self, key : str, value : object = None
     ) :
        if key in self.cache : 
                self.cache.move_to_end(key)
        self.cache[key] = value

        if len(self.cache) > self.capacity :
            self.cache.popitem(last=False)    


    def __len__(self) -> int:
         return len(self.cache)    
