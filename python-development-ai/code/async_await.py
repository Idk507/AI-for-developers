"""
=============================================================================
 ASYNC / AWAIT — The Heartbeat of Every LLM Application
=============================================================================

Real-World Context:
    Every GenAI app is fundamentally an I/O waiting machine.
    - You call an LLM API           → wait 1–5s
    - You query a vector database   → wait 100–400ms
    - You hit an embedding service  → wait 50–200ms

    Without async: serve ONE user at a time. During each wait, everything freezes.
    With async:    serve THOUSANDS concurrently on a SINGLE thread.

    This is the single most impactful concept in Python GenAI development.

Topics Covered:
    1.1  Coroutines — what async def actually does
    1.2  Event Loop — asyncio's scheduler
    1.3  Tasks & Futures — parallel RAG retrieval
    1.4  Async Generators — streaming LLM tokens
    1.5  Async Context Managers — safe resource cleanup
    1.6  Timeout + Retry — production resilience
=============================================================================
"""

import os
import re
import sys

import json
import random
import time
import uuid
from dataclasses import dataclass
from typing import AsyncGenerator, Literal, Optional

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p) != script_dir]

import asyncio

from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    def load_dotenv() -> bool:
        return False

load_dotenv()


def extract_text_from_response(response) -> str:
    candidates = []

    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        candidates.append(output_text.strip())

    for item in getattr(response, "output", []) or []:
        content_blocks = getattr(item, "content", None) or []
        for block in content_blocks:
            text_value = getattr(block, "text", None)
            if isinstance(text_value, str) and text_value.strip():
                candidates.append(text_value.strip())
            elif isinstance(text_value, dict):
                nested = text_value.get("text")
                if isinstance(nested, str) and nested.strip():
                    candidates.append(nested.strip())
            elif isinstance(block, dict):
                nested_text = block.get("text")
                if isinstance(nested_text, str) and nested_text.strip():
                    candidates.append(nested_text.strip())

    return "\n".join(candidates)


def parse_triage_payload(raw_text: str) -> dict[str, str]:
    if not raw_text:
        return {}

    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return {str(k): str(v) for k, v in data.items() if isinstance(v, (str, int, float, bool))}
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.S)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items() if isinstance(v, (str, int, float, bool))}
        except json.JSONDecodeError:
            pass

    return {}


def get_azure_openai_config():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") "
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT") or "gpt-4o"

    try:
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    except ImportError:
        return None, deployment_name, None, endpoint

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default",
    )

    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider,
    )

    return client, deployment_name, None, endpoint


# COROUTINEs -the building blocks of async/await

@dataclass
class PatientCase:
    patient_id: str
    symptoms: str
    age: str


@dataclass
class TriageResult:
    patient_id: str
    urgency: Literal["critical", "high", "medium", "low"]
    advice: str
    latency_ms: float

async def assess_patient(case: PatientCase) -> TriageResult:
    """
    Coroutine: sends one patient case to Azure OpenAI for urgency triage.

    REAL USE CASE: A hospital emergency department receives 200 patients
    simultaneously during a mass-casualty event. This coroutine is called
    for each patient. Without async, patient 200 waits 200×3s = 10 minutes.
    With async, ALL patients get a response in ~3 seconds.

    HOW IT WORKS:
        - 'async def' makes this a coroutine function
        - Calling assess_patient(case) returns a coroutine OBJECT (not executed yet)
        - The coroutine runs only when you 'await' it inside an event loop
        - At 'await client.messages.create(...)': this coroutine PAUSES
          and hands control back to the event loop
        - The event loop runs OTHER coroutines (other patients) during the wait
        - When the API responds, this coroutine RESUMES from the await point

    WHY NOT THREADS?
        - 200 threads = 200× memory + OS context switch overhead
        - async = 1 thread, zero OS overhead, same concurrency

    Args:
        case: Patient data including symptoms and age

    Returns:
        TriageResult with urgency level and clinical advice
    """
    start = time.perf_counter()  # perf_counter is a high-resolution timer for measuring elapsed time

    def fallback_triage() -> tuple[str, str]:
        if any(w in case.symptoms for w in ["chest pain", "can't breathe", "unconscious"]):
            return "critical", "Call 911 immediately. Do not move patient."
        if any(w in case.symptoms for w in ["fever", "vomiting", "severe"]):
            return "high", "See a doctor within 2 hours."
        if any(w in case.symptoms for w in ["headache", "nausea", "rash"]):
            return "medium", "Schedule same-day appointment."
        return "low", "Monitor symptoms, rest at home."

    client, deployment_name, _, _ = get_azure_openai_config()
    if client is None:
        urgency, advice = fallback_triage()
        latency = (time.perf_counter() - start) * 1000
        return TriageResult(case.patient_id, urgency, advice, latency)

    try:
        response = await asyncio.to_thread(
            client.responses.create,
            model=deployment_name,
            input=(
                "Assess urgency as critical/high/medium/low. "
                "Reply JSON with keys urgency and advice. "
                f"Patient {case.age}yo. Symptoms: {case.symptoms}"
            ),
        )
        raw_text = extract_text_from_response(response)
        data = parse_triage_payload(raw_text)
        urgency = data.get("urgency") or fallback_triage()[0]
        advice = data.get("advice") or fallback_triage()[1]
    except Exception as exc:
        print(f"[AZURE] Azure OpenAI call failed: {exc}")
        urgency, advice = fallback_triage()

    await asyncio.sleep(random.uniform(0.5, 2.0))

    latency = (time.perf_counter() - start) * 1000
    return TriageResult(case.patient_id, urgency, advice, latency)



async def run_triage_batch(cases: list[PatientCase]) -> list[TriageResult]:
    """
    Runs ALL patient assessments CONCURRENTLY using asyncio.gather().

    KEY INSIGHT: Without gather(), you'd write:
        for case in cases:
            result = await assess_patient(case)  # waits 2s, THEN moves to next

    With gather(), ALL coroutines start simultaneously:
        results = await asyncio.gather(*[assess_patient(c) for c in cases])
        # 20 patients × 2s each = 2s total (not 40s!)

    asyncio.gather() also accepts return_exceptions=True to prevent
    one failure from cancelling all other concurrent operations.

    Args:
        cases: List of patient cases to assess

    Returns:
        List of triage results sorted by urgency (critical first)
    """
    print(f"\n[TRIAGE] Starting concurrent assessment of {len(cases)} patients...")
    t_start = time.perf_counter()

    # All coroutines fire simultaneously — event loop juggles them
    results = await asyncio.gather(
        *[assess_patient(c) for c in cases],
        return_exceptions=True   # don't abort ALL if one fails
    )

    # Filter out any exceptions
    valid = [r for r in results if isinstance(r, TriageResult)]
    total_time = (time.perf_counter() - t_start) * 1000
    print(f"[TRIAGE] {len(valid)} patients assessed in {total_time:.0f}ms "
          f"(sequential would take ~{len(valid) * 1250:.0f}ms)")

    # Sort: critical first
    priority = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(valid, key=lambda r: priority[r.urgency])

# =============================================================================
# 1.2  EVENT LOOP — asyncio's scheduler
# =============================================================================

async def demonstrate_event_loop():
    """
    Shows how the event loop switches between coroutines cooperatively.

    REAL USE CASE: FastAPI runs one event loop per process. Every HTTP
    request becomes a coroutine on that loop. With async LLM calls, a
    single FastAPI process can handle 500 simultaneous users — impossible
    with synchronous code.

    HOW THE EVENT LOOP WORKS:
        1. You call asyncio.run(main()) → creates a new event loop
        2. Loop starts running 'main' coroutine
        3. When 'main' hits 'await', it suspends and loop picks next ready task
        4. Loop keeps cycling until all tasks complete
        5. asyncio.run() destroys the loop and returns

    COOPERATIVE vs PREEMPTIVE:
        - OS threads: preemptive (OS forcefully switches threads)
        - asyncio:    cooperative (coroutine VOLUNTARILY yields at await)
        - Risk: if you do CPU-heavy work without awaiting, you BLOCK the loop
    """
    loop = asyncio.get_running_loop()
    print(f"\n[LOOP] Running loop: {type(loop).__name__}")
    print(f"[LOOP] Is running: {loop.is_running()}")

    async def task_a():
        print("[LOOP] Task A: starting work")
        await asyncio.sleep(0.1)   # yield to loop — Task B can run here
        print("[LOOP] Task A: resumed and finishing")
        return "A done"

    async def task_b():
        print("[LOOP] Task B: starting work")
        await asyncio.sleep(0.05)  # Task A still waiting, but B can run
        print("[LOOP] Task B: resumed and finishing")
        return "B done"

    # create_task() schedules immediately WITHOUT awaiting
    # The coroutine starts running in the BACKGROUND
    task1 = asyncio.create_task(task_a(), name="EmailClassifier")
    task2 = asyncio.create_task(task_b(), name="DraftGenerator")

    print(f"[LOOP] Tasks created: {task1.get_name()}, {task2.get_name()}")
    print("[LOOP] Doing other work while tasks run in background...")

    # Now collect results (blocks until both complete)
    results = await asyncio.gather(task1, task2)
    print(f"[LOOP] Results: {results}")

    # Tasks & Futures - parallel RAG retrieval


@dataclass
class RetrievalHit:
    source : str
    content : str
    relevance_score : float

async def search_vector_db(query: str) -> list[RetrievalHit]:
    """
    Searches a vector database (Pinecone/Qdrant/Weaviate) for relevant docs.

    REAL USE CASE: Legal research assistant querying a database of 10M
    court case embeddings. Typical latency: 200–400ms.

    In a real implementation:
        import qdrant_client
        client = qdrant_client.AsyncQdrantClient(url="http://localhost:6333")
        results = await client.search(
            collection_name="case_law",
            query_vector=await embed(query),
            limit=5
        )
    """
    await asyncio.sleep(0.3)  # Simulates vector DB query latency
    return [
        RetrievalHit("case_law_db", f"Smith v Jones (2019): precedent for '{query[:20]}'", 0.92),
        RetrievalHit("case_law_db", f"Doe v State (2021): related to '{query[:20]}'", 0.87),
    ]



async def search_statutes(query: str) -> list[RetrievalHit]:
    """Queries a structured statute database. Typically 150–250ms."""
    await asyncio.sleep(0.2)
    return [RetrievalHit("statute_db", f"§ 42 USC 1983: applies to '{query[:20]}'", 0.88)]


async def search_recent_news(query: str) -> list[RetrievalHit]:
    """Fetches recent news for current context. Typically 400–600ms."""
    await asyncio.sleep(0.5)
    return [RetrievalHit("web_search", f"Recent ruling on '{query[:20]}' (2025)", 0.75)]


async def legal_rag_pipeline(legal_question: str) -> str:
    """
    Full RAG pipeline with parallel retrieval using Tasks.

    REAL USE CASE: A legal AI product serving lawyers. Each query must
    search 3 different sources. Without parallelism:
        300ms + 200ms + 500ms = 1000ms per query

    With create_task() parallelism:
        max(300, 200, 500) = 500ms per query  ← 2x faster

    At 10,000 queries/day: saves ~83 minutes of user wait time daily.

    TASK vs GATHER:
        - asyncio.gather():    convenient, waits for ALL, returns list
        - asyncio.create_task(): more control, tasks start immediately,
          you await them when you need the results

    Choose create_task() when:
        - You want to do other work between starting and awaiting tasks
        - You need to cancel specific tasks
        - Tasks have different lifetimes

    Args:
        legal_question: The legal question to research

    Returns:
        A synthesized answer with citations from all three sources
    """
    print(f"\n[RAG] Starting parallel retrieval for: '{legal_question[:50]}'")
    t_start = time.perf_counter()

    # Fire all three retrievals SIMULTANEOUSLY
    # These lines return immediately — tasks start in background
    task_cases    = asyncio.create_task(search_vector_db(legal_question))
    task_statutes = asyncio.create_task(search_statutes(legal_question))
    task_news     = asyncio.create_task(search_recent_news(legal_question))

    # While retrieval runs in background, do synchronous prep
    system_prompt = (
        "You are an expert legal research assistant. "
        "Cite specific cases and statutes. Be precise."
    )

    # Now collect — blocks until EACH task completes
    cases    = await task_cases     # unblocks at 300ms
    statutes = await task_statutes  # already done at 300ms (finished at 200ms)
    news     = await task_news      # blocks until 500ms

    elapsed = (time.perf_counter() - t_start) * 1000
    print(f"[RAG] All sources retrieved in {elapsed:.0f}ms "
          f"(sequential would be ~1000ms)")

    # Assemble context
    all_hits = cases + statutes + news
    all_hits.sort(key=lambda h: h.relevance_score, reverse=True)
    context = "\n".join(f"[{h.source}] {h.content}" for h in all_hits)

    # In production: await real LLM call here
    return f"Based on {len(all_hits)} sources:\n{context}\n\nSYSTEM: {system_prompt}"


# Async Generators — streaming LLM tokens

async def stream_code_review(code : str, language : str) -> AsyncGenerator[str,None]:
    """
    Async generator that yields code review tokens as they arrive from the LLM.

    REAL USE CASE: A VS Code extension that shows AI code review in real time.
    Without streaming: user stares at spinner for 8–15 seconds.
    With streaming: feedback appears token by token starting in 0.5s.
    UX improvement: perceived latency drops from 10s to 0.5s (95% better).

    HOW ASYNC GENERATORS WORK:
        - 'async def' + 'yield' = async generator function
        - Returns an async generator object (not executed yet)
        - Each 'async for token in stream_code_review(...)' call:
            1. Resumes the generator
            2. Runs until next 'yield token'
            3. Returns that token to caller
            4. Pauses again

    REAL ANTHROPIC SDK STREAMING:
        async with client.messages.stream(
            model="claude-opus-4-5",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            async for text_chunk in stream.text_stream:
                yield text_chunk   # forward each token immediately

    Args:
        code:     Source code to review
        language: Programming language of the code

    Yields:
        Individual tokens/chunks of the code review as they arrive
    """
    # Simulate streaming response from Claude
    review_tokens = (
        f"## Code Review for {language.upper()} Code\n\n"
        "**Security Issues Found:**\n"
        f"- Line 3: SQL injection vulnerability detected in `{code[:20].strip()}...`\n"
        "  Fix: Use parameterised queries instead of f-strings\n\n"
        "**Performance Issues:**\n"
        "- No connection pooling configured\n"
        "- Missing database indices on queried columns\n\n"
        "**Recommendations:**\n"
        "1. Use `?` placeholders: `cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))`\n"
        "2. Add `@lru_cache` for frequently called queries\n"
        "3. Implement connection pool with `pool_size=10`\n"
    ).split()  # Split into words to simulate token stream

    # Simulate token-by-token streaming (50-150ms between tokens)
    for i, token in enumerate(review_tokens):
        await asyncio.sleep(0.05)   # Simulates inter-token delay from LLM
        yield token + (" " if i < len(review_tokens) - 1 else "")



async def stream_to_vscode(code: str):
    """
    Demonstrates the producer/consumer streaming pattern using asyncio.Queue.

    REAL USE CASE: A Language Server Protocol (LSP) server streams LLM
    review tokens to VS Code over a WebSocket. The queue decouples:
    - Producer: receives tokens from Claude API
    - Consumer: sends tokens to the editor via WebSocket

    This pattern prevents backpressure issues — if the UI is slow to
    consume, the queue buffers tokens without blocking the API stream.

    asyncio.Queue vs asyncio.gather:
        - gather: run multiple coroutines, collect all results at end
        - Queue:  decouple producer and consumer with buffering
        Use Queue when producer and consumer run at different speeds.
    """
    print(f"\n[STREAM] Starting code review stream...")
    queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=50)
    full_review = []

    async def producer():
        """Fetches tokens from Claude and buffers them in the queue."""
        async for token in stream_code_review(code, "python"):
            await queue.put(token)
        await queue.put(None)  # Sentinel: signals stream is complete

    async def consumer():
        """Drains the queue and 'sends' tokens to the VS Code extension."""
        while True:
            token = await queue.get()
            if token is None:
                break
            full_review.append(token)
            print(token, end="", flush=True)  # → websocket.send(token) in prod
            queue.task_done()

    # Producer and consumer run concurrently on the same event loop
    await asyncio.gather(producer(), consumer())
    print(f"\n[STREAM] Complete. Total tokens streamed: {len(full_review)}")
    return "".join(full_review)

# Async context managers — safe resource cleanup

class AsyncHTTPSession:
    """
    Simulates an async HTTP session (like aiohttp.ClientSession).

    REAL USE CASE: An embedding microservice that processes thousands of
    requests. Each request reuses a shared aiohttp.ClientSession for
    connection pooling instead of opening a new TCP connection each time.
    This reduces latency by ~40ms and prevents socket exhaustion.

    In production:
        async with aiohttp.ClientSession() as session:
            # Session reuses connections from pool
            async with session.post(url, json=payload) as resp:
                return await resp.json()
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._pool_size = 0
        self.session_id = str(uuid.uuid4())
        print(f"[SESSION] Created session {self.session_id} for {self.base_url}")
    async def __aenter__(self):
        """
        Called when entering 'async with AsyncHTTPSession(...) as session'.
        Opens connection pool, authenticates, sets up headers.
        """
        print(f"[HTTP] Opening connection pool to {self.base_url}")
        await asyncio.sleep(0.01)  # Simulates pool initialization
        self._pool_size = 10
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Called when leaving the 'async with' block — even if an exception occurred.
        Guarantees connection pool is closed, preventing resource leaks.

        exc_type/exc_val/exc_tb are non-None if an exception occurred.
        Returning True suppresses the exception (usually don't want this).
        """
        print(f"[HTTP] Closing connection pool ({self._pool_size} connections)")
        await asyncio.sleep(0.01)  # Simulates pool teardown
        self._pool_size = 0
        # Return False (implicitly) to let exceptions propagate
    async def post(self, endpoint: str, payload: dict) -> dict:
        if self._pool_size == 0:
            raise RuntimeError("Session not active — use 'async with'")
        await asyncio.sleep(0.1)  # Simulates HTTP round trip
        return {"embedding": [0.1] * 1536, "model": "text-embedding-3-small"}


async def embed_documents_with_session(texts : list[str]) -> list[list[float]]:
    """
    Embeds multiple documents sharing one hTTP session (Connection pooling).

    without async context_manager:
        for text in texts:
            response = requests.post(url, json={"text": text}) # new TCP connection each time   
        # if exception thrown mid-loop : connections leak , never closed

    with async context_manager: 
        async with AsyncHTTPSession(url) as session:
            for text in texts:
                response = await session.post("/embed", {"text": text}) # reuses connection pool
                yield response["embedding"]
            # connection pool shared across all requests, closed automatically at exit
            # Guarantees no resource leaks even if an exception occurs mid-loop
    """
    embeddings = []
    url = "https://api.openai.com/v1/embeddings"
    async with AsyncHTTPSession(url) as session:
        # All requests share the connection pool — efficient
        tasks = [
            session.post("/embeddings", {"input": text, "model": "text-embedding-3-small"})
            for text in texts
        ]
        results = await asyncio.gather(*tasks)
        embeddings = [r["embedding"] for r in results]

    # Here: session is guaranteed closed, pool is freed
    print(f"[EMBED] Embedded {len(embeddings)} documents,   session closed cleanly")
    return embeddings

# Timeout + Retry — production resilience

async def generate_with_retry(
    prompt : str, max_attempts : int = 4,
    timeout_sec : float = 10.0,
    base_delay : float = 1.0
) -> str :
    """
    Calls an LLM with per-attempt timeouts and exponential backoff.

    REAL USE CASE: An e-commerce AI generating product descriptions.
    During Black Friday, API rate limits cause 30% of calls to fail.
    Without retry: 30% of product pages show broken descriptions.
    With exponential backoff: 99.9% succeed within 15 seconds.

    WHY EXPONENTIAL BACKOFF + JITTER?
        - Simple retry (all wait 1s): 1000 clients all retry at t=1s
          → burst of 1000 requests hits server simultaneously → DDoS!
        - Exponential (1s, 2s, 4s, 8s): load spreads over time
        - Jitter (add randomness): prevents synchronized retries
          even if many clients started at the same time

    WHY asyncio.wait_for()?
        - Without it: a stuck API call hangs FOREVER, blocking the loop
        - wait_for(coro, timeout=10): cancels cleanly after 10s
        - Raises asyncio.TimeoutError (catchable)

    Args:
        prompt:       Prompt to send to the LLM
        max_attempts: Total number of attempts before giving up
        timeout_sec:  Per-attempt timeout (avoids infinite hangs)
        base_delay:   Starting retry delay (doubles each attempt)

    Returns:
        LLM response text

    Raises:
        RuntimeError: If all attempts are exhausted
    """
    last_error = None
    for attempt in range(max_attempts):
        try :
            print(f"[RETRY] Attempt {attempt + 1}/{max_attempts} for prompt: '{prompt[:30]}...'")
            # simulate an llm call that sometimes fails / hangs
            async def fake_llm_call():
                roll = random.random()
                if roll < 0.3 :
                    raise ConnectionError("Rate Limit Exceeded (429)")
                if roll < 0.5 :
                    await asyncio.sleep(timeout_sec + 5)  # Simulate a hang
                await asyncio.sleep(random.uniform(0.5, 1.5))  # Simulate normal latency
                return f"LLM response for '{prompt[:30]}...'"

        except asyncio.TimeoutError:
            last_error = asyncio.TimeoutError("Request timed out")
            print(f"[RETRY] Timeout on attempt {attempt + 1}. Retrying...")
        
        except ConnectionError as e :
            last_error = e
            print(f"[RETRY] Connection error on attempt {attempt + 1}: {e}. Retrying...")
        if attempt < max_attempts - 1:
            delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0, 0.5)  # Add up to 0.5s of randomness
            wait = delay + jitter # jitter prevents thundering herd problem (thundering herd problem: many clients retrying at the same time)
            print(f"[RETRY] Waiting {wait:.2f}s before next attempt...")
            await asyncio.sleep(wait)

    raise RuntimeError(
        f"All {max_attempts} attempts failed. Last error: {last_error}"
    )



# main - async main()
async def main():
    print("Section 1 : Async /Await for Genai applications")

    # 1.1 Coroutines
    patients = [
        PatientCase("P001", "chest pain, shortness of breath", 62),
        PatientCase("P002", "mild headache, runny nose", 28),
        PatientCase("P003", "high fever 104F, stiff neck", 5),
        PatientCase("P004", "ankle sprain, mild swelling", 34),
        PatientCase("P005", "unconscious, trauma to head", 45),
    ]
    results = await run_triage_batch(patients)
    for r in results :
        print(f"Patient {r.patient_id}: Urgency={r.urgency}, Advice='{r.advice}', Latency={r.latency_ms:.0f}ms")
    
    # 1.2 Event Loop
    print("\n--- Demonstrating Event Loop ---")
    print("Event loop allows multiple coroutines to run concurrently on a single thread.")
    await demonstrate_event_loop()

    #1.3 Tasks & Futures
    print("\n--- Demonstrating Tasks & Futures ---")
    print("Tasks allow parallel retrieval of data from multiple sources.")
    legal_question = "Can police search y phone without a warrant?"
    answer = await legal_rag_pipeline(legal_question)
    print(f"\n[RAG] Synthesized Answer:\n{answer}")

    #1.4 Async Streaming
    print("\n--- Demonstrating Async Streaming ---")
    sample_code = "def get_user_data(user_id):\n    return db.query(f'SELECT * FROM users WHERE id = {user_id}')"
    review = await stream_to_vscode(sample_code)
    print(f"\n[STREAM] Full Review:\n{review}")

    #1.5 Async Context Managers
    print("\n--- Demonstrating Async Context Managers : Session pooling embeddings ---")
    documents = [
        "Document 1: The quick brown fox jumps over the lazy dog.",
        "Document 2: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Document 3: Python is a versatile programming language."
    ]
    embeddings = await embed_documents_with_session(documents)

    #1.6 Timeout + Retry
    print("\n--- Demonstrating Timeout + Retry ---")
    try : 
        result = await generate_with_retry("Generate a product description for a new smartwatch.")
        print(f"[RETRY] LLM Response: {result}")
    except RuntimeError as e :
        print(f"[RETRY] All attempts failed: {e}")


asyncio.run(main())



