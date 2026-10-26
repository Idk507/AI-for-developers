Imagine you're designing an enterprise RAG assistant that uses a vector database, an LLM inference API, and several external tools.

The vector database is healthy, but the LLM inference API begins returning intermittent timeout errors.

Your application currently retries every failed inference request three times.

As traffic increases, the application experiences growing latency and a rising number of failed requests.

Interview scenario: Explain how you would combine request timeouts, retry policies, circuit breakers, and fallback responses to maintain service reliability.

Your explanation should address when a retry is appropriate, when the circuit should open, how the system detects recovery, and what response users should receive when inference is unavailable.

Also consider how you would monitor the system using latency percentiles, failure rates, circuit-state transitions, and distributed traces.