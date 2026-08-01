
=============================================================================
FILE MAP
=============================================================================

section_01_async_await.py
    1.1  Coroutines              — Hospital triage: 5 patients, 1 thread, concurrent
    1.2  Event Loop              — Email assistant: cooperative scheduling explained
    1.3  Tasks & Futures         — Legal RAG: parallel vector + statute + web retrieval
    1.4  Async Generators        — VS Code code reviewer: real-time token streaming
    1.5  Async Context Managers  — Embedding service: connection pool reuse
    1.6  Timeout + Retry         — E-commerce AI: exponential backoff on rate limits

section_02_threading.py
    2.1  GIL Deep Dive           — QA system: what the GIL releases vs holds
    2.2  Lock                    — Multi-tenant AI: thread-safe API budget tracking
    2.3  RLock                   — Recursive pipeline stages that call each other
    2.4  Event + Semaphore       — Video moderation: model-ready gate + GPU slot limit
    2.5  Condition               — Batch embedding queue: wait for N items or timeout
    2.6  ThreadPoolExecutor      — Image generation: 12 images, 5 workers, as_completed
    2.7  Thread-local storage    — Inference server: per-thread model instances

section_03_04_05_multiprocessing_generators_decorators.py
    3.1  Process vs Thread       — CPU-bound regex: why threads don't help here
    3.2  ProcessPoolExecutor     — Wikipedia preprocessing: tokenise 10K docs in parallel
    3.3  Shared Memory           — Embedding index: zero-copy 6GB matrix across processes
    4.1  Generator Functions     — Common Crawl pipeline: 500GB in O(1) memory
    4.2  Composing Generators    — extract → clean → deduplicate → batch (lazy chain)
    4.3  Generator Expressions   — Memory comparison: list vs generator for embeddings
    4.4  itertools               — chain shards · islice sampling · cycle epochs · product grid
    5.1  Decorator Factories     — Compliance logging: trace every LLM call automatically
    5.2  validate_prompt         — Prompt injection defence at the decorator layer
    5.3  functools.wraps         — Preserving __name__, __doc__, __signature__
    5.4  lru_cache               — Financial QA: cache embeddings, save $400/day
    5.5  Async-safe cache        — Double-checked locking to prevent thundering herd
    5.6  functools.partial       — Create extract_figures, write_summary, flag_risks callers
    5.7  functools.reduce        — Compose text normalisation pipeline into one callable

section_06_to_10_advanced.py
    6.1  @contextmanager         — OpenTelemetry-style spans with nested timing
    6.2  asynccontextmanager     — Persistent LLM connection with guaranteed teardown
    6.3  ExitStack               — LLaMA-70B: load 14 shards, all closed on any exit
    7.1  Dataclasses             — LLMResponse with cost/throughput computed properties
    7.2  Pydantic                — Entity extraction: validate LLM JSON at runtime
    7.3  Protocols + Generics    — Swap OpenAI for Cohere without changing RAG code
    8.1  __slots__               — Token objects: 40% smaller, 176MB saved per 1M tokens
    8.2  weakref                 — Adaptive embedding cache: auto-evicts under memory pressure
    8.3  tracemalloc             — Find exactly which line is causing a memory leak
    9.1  Metaclass               — LLM provider registry: auto-register on class definition
    9.2  Descriptors             — Prompt template slots: validate at assignment time
    9.3  Dunder methods          — Pipeline DSL: strip | lowercase | tokenize | count
   10.1  Hybrid pipeline         — asyncio fetch + ProcessPool PDF extract + async Claude
   10.2  Rate limiter            — Token bucket: 60 RPM cap with Semaphore concurrency
   10.3  Supervisor pattern      — Resilient workers: auto re-queue failed jobs

=============================================================================
QUICK DECISION GUIDE
=============================================================================

  Task                            Tool
  ─────────────────────────────── ────────────────────────────────────────
  Concurrent LLM API calls        asyncio + asyncio.gather()
  Stream tokens to UI             async generator + async for
  Parallel embed (blocking lib)   ThreadPoolExecutor (GIL releases on C ops)
  Tokenise millions of docs       ProcessPoolExecutor + initializer
  Multi-GB training datasets      Generator pipeline (O(1) memory)
  Cache embedding API calls       @lru_cache (sync) or double-checked dict (async)
  LLM rate limiting               TokenBucketRateLimiter + asyncio.Semaphore
  Structured LLM JSON output      Pydantic BaseModel with validators
  Retry on API errors             @retry decorator with exponential backoff
  GPU/DB cleanup on error         @contextmanager / ExitStack
  Swap LLM providers              Protocol + Generic TypeVar
  Zero-copy embedding matrices    multiprocessing.shared_memory + numpy
  Mixed I/O + CPU pipeline        asyncio + loop.run_in_executor(ProcessPool)
  Dynamic provider selection      Metaclass registry
  Memory-efficient token objects  __slots__ or NamedTuple
  Find memory leaks               tracemalloc + gc.collect()
=============================================================================
