Imagine you're designing a RAG system for 10,000 enterprise users.

The system retrieves documents from a vector database and generates responses using an LLM.

To reduce latency and cost, you decide to introduce caching.

Your interview question is:

Would you use TTL caching, LRU caching, or both? Explain where each strategy would be useful and what could go wrong.

Think about document freshness, memory limits, cache invalidation, and authorization.

One particularly important security concern is whether two users with different document permissions should ever share the same cached retrieval results.

In a production system, cache keys and retrieval authorization must account for tenant and access boundaries. Cached content should not bypass the permissions that would apply to a fresh retrieval.