"""
=============================================================================
 THREADING — When Your Library Doesn't Speak Async
=============================================================================

Real-World Context:
    Many powerful AI libraries are BLOCKING — you can't await them:
    - HuggingFace Transformers (inference pipeline)
    - LangChain synchronous tools
    - psycopg2 (PostgreSQL driver)
    - PIL/Pillow (image processing)
    - Some vector DB clients

    Threading lets you parallelise these WITHOUT rewriting them as async.

    CRITICAL DISTINCTION:
    - Async = single thread, cooperative switching at await points
    - Threads = multiple threads, OS switches between them preemptively
    - For BLOCKING I/O or C-extension work → threads win

Topics Covered:
    2.1  The GIL — what it blocks and what it releases
    2.2  Lock — mutual exclusion for shared counters
    2.3  RLock — re-entrant locking for recursive pipelines
    2.4  Event — model-ready signalling
    2.5  Semaphore — GPU slot limiting
    2.6  Condition — producer/consumer batching
    2.7  ThreadPoolExecutor — parallel image generation
    2.8  Thread-local storage — per-thread model instances
=============================================================================
"""
import sys
import threading 
import time
import queue 
import random 
from concurrent.futures import ThreadPoolExecutor, as_completed 
# concurrent is a higher-level interface for threading, multiprocessing, and async. It provides ThreadPoolExecutor and ProcessPoolExecutor for parallel execution of tasks.
from typing import List ,Any,Optional 
from dataclasses import dataclass, field

# GIL - Global Interpreter Lock
def demonstrate_gil():
    """
    Demonstrates what the GIL blocks and what it allows.

    REAL USE CASE: A manufacturing QA system runs ML model inference
    on defect images. The model uses C-level PyTorch ops that release
    the GIL, so 8 threads genuinely run their inference in parallel.

    GIL RELEASES DURING:
        ✅ All network I/O (HTTP calls, socket reads/writes)
        ✅ File system operations (reading training data)
        ✅ NumPy/PyTorch C operations (the actual ML computation)
        ✅ time.sleep() calls
        ✅ Any call into a C extension that releases it explicitly

    GIL IS HELD DURING:
        ❌ Pure Python loops: for i in range(1_000_000): total += i
        ❌ Python-level string/list/dict operations
        ❌ Python-level arithmetic
        ❌ Any bytecode execution

    CONSEQUENCE FOR AI:
        - Threading WORKS for: HuggingFace inference, NumPy ops, I/O
        - Threading DOESN'T HELP for: pure Python tokenization, parsing
        - For pure Python CPU work → use multiprocessing (Section 3)
    """
    print(f"GIL implementation details: {sys.implementation.version}")
    print(f"Python version: {sys.version}")
    print("GIL releases during network I/O, file I/O, and C extensions.")

    results = {}
    lock = threading.Lock()

    def worker_io_bound(thread_id : int):
        """
        I/O - bound work : GIL released during time.sleep() (simulates network I/O).
        Multiple threads can make real progress simultaneously here.
        """
        start = time.perf_counter() # perf_counter - high-resolution timer for measuring short durations
        time.sleep(random.uniform(0.1, 0.5)) # Simulate I/O delay
        elapsed = (time.perf_counter() - start)*1000
        with lock :
            results[thread_id] = elapsed
            print(f"[I/O] Thread {thread_id} finished in {elapsed:.2f} ms")
    # 5 threads , each sleeping 200ms 
    # sequentials : 5 * 200ms = 1000ms
    # parallel : 200ms (all threads sleep simultaneously)
    # with threads (GIL releases on sleep) : ~200ms total
    print("\n[GIL] Running 5 I/O-bound threads (GIL releases on I/O):")
    t_start = time.perf_counter()
    threads = [threading.Thread(target=worker_io_bound, args=(i,)) for i in range(5)]
    for t in threads : t.start()
    for t in threads : t.join()
    total  = (time.perf_counter() - t_start)*1000
    print(f"[GIL] Total time for I/O-bound threads: {total:.2f} ms\n")


#  2 - lock - protecting shared counters 

@dataclass
class APIUsageTracker:
    """
    Tracks API call counts and costs across mulitple threads
    REAL use case : A multi tenant AI platform where 50 concurrent threads each make LLM calls. 
    1.Track total api calls (for billing)
    2.track total tokens used (for rate limiting)
    3.block when monthly budget is exceeded

    without lock : two threads read count = 100 simultaneously both add 1 and both write 101 .Actual count should be 102. BUG!

    With LOCK : only one thread can read modify write at a time .Safe 
    """
    _call_count : int = 0
    _token_count : int = 0 
    _cost_usd : float = 0.0 
    _lock : threading.lock = field(deafault_factory = threading.Lock)
    monthly_budget : float = 1000.0

    def record_call(self, input_tokens : int, output_tokens : int) -> bool:
            """
            Thread-safe recording of an LLM API call.

        'with self._lock' is equivalent to:
            self._lock.acquire()
            try:
                <body>
            finally:
                self._lock.release()

        The Lock guarantees that only ONE thread is inside this
        block at any time. All others BLOCK at the 'with' line.

        Returns:
            True if call was recorded, False if budget exceeded
            """
            # cost in usd 
            call_cost = (input_tokens * 3e-6) + (output_tokens * 15e-6)
            with self._lock : # only one thread enters at a time 
                if self._cost_usd + call_cost > self.monthly_budget :
                    print(f"[LOCK] Budget exceeded !" 
                        f"USed : {self._cost_usd:.2f}, limit:{self.monthly_budget}")
                    return False 
                self._call_count += 1
                self._token_count += input_tokens + output_tokens
                self._cost_usd += call_cost
                return True 
            
            @property #
            def stats(self) -> dict :
                with self._lock:
                    return {
                        "calls": self._call_count,
                        "tokens" : self._token_count,
                        "cost_usd": round(self._cost_usd,4)
                    }


def simulate_concurrent_llm_calls():
    """
    Simulates 20 threads making LLM calls concurrently with budget tracking.

    REAL USE CASE: A customer support AI where multiple agent threads
    handle different tickets simultaneously. All share one API budget tracker.
    """
    tracker = APIUsageTracker(monthly_budget=0.01) # low budget to trigger limit 
    success_count = 0 
    count_lock = threading.Lock()

    def handle_support_ticket(ticket_id : int):
        nonlocal success_count 
        #simulate varying token usage per ticket 
        input_tok = random.randint(100, 500)
        output_tok = random.randint(50,300)
        time.sleep(random.uniform(0.01,0.05)) # simulate api call time

        ok = tracker.record_call(input_tok, output_tok)
        if ok :
            with count_lock:
                success_count +=1
        
    print("\n [LOCK] Runnin 20 concurrent support ticket handlers")

    threads = [
        threading.Thread(target = handle_support_ticket, args=(i)) for i in range(20)
    ]
    for t in threads : t.start()
    for t in threads : t.join()

    print(f"LOCK stats : {tracker.stats}")
    print(f"[LOCK] successful calls : {success_count}/20")


# RLOCK - re-entrant lock for recursive pipelines

class PieplineStageLogger:
        """
        A logging system for nested pipeline stages that can safely call each other.

        REAL USE CASE: A document processing pipeline where stages can call
        sub-stages. Stage A (preprocess) calls Stage B (clean), which calls
        Stage C (tokenise). If all three share a regular Lock, Stage A would
        deadlock when B tries to acquire the same lock A already holds.

        RLock (Re-entrant Lock) allows the SAME THREAD to acquire it multiple
        times. It tracks a counter — acquired N times, must release N times.
        """
        def __init__(self):
            self._rlock = threading.RLock()  # Re-entrant: same thread can re-acquire
            self._log_entries = []

        def log_stage(self, stage_name: str, action: str):
            """
            Can be called from nested pipeline stages on the same thread.

            With threading.Lock(): deadlock if log_stage calls log_stage
            With threading.RLock(): same thread re-enters safely
            """
            with self._rlock:
                entry = f"[{stage_name}] {action}"
                self._log_entries.append(entry)

                # This nested call re-acquires the SAME rlock on the SAME thread
                # With Lock: DEADLOCK. With RLock: works fine.
                if "ERROR" in action:
                    self.log_stage("ERROR_HANDLER", f"Handling error in {stage_name}")

        def get_logs(self) -> list[str]:
            with self._rlock:
                return self._log_entries.copy()


# Event - model ready signalling

class ModelServer:
    """
    An inference server that loads a model in the background while workers wait.
    
        REAL USE CASE: A video content moderation system that starts 20 worker
        threads to process an incoming batch. The model takes 3 seconds to load.
        Workers should start immediately but wait at the gate until model is ready,
        then ALL rush through simultaneously once it's loaded.
    
        threading.Event is perfect for this "gate" pattern:
        - event.wait() : blocks until event is set (the gate is closed)
        - event.set()  : unblocks ALL waiting threads at once (open the gate)
        - Unlike Lock, Event doesn't "consume" the signal — all waiters unblock

        threading.Event() - 
        threading.Semaphore() - 
        threading.Thread()  - 

        """
    def __init_(self):
        self._ready_event = threading.Event()
        self._model = None 
        self._inference_semaphore = threading.Semaphore(3) # max 3 concurrent , semaphore 
    
    def load_model_in_background(self):
        """ load the model in a daemon thread while workers start up""" 
        def _load():
            print("[MODEL] Loading model weights from disk")
            time.sleep(2.0)
            self._model = lambda text : "FLAGGED"  if len(text) > 50 else "SAFE"
            print("[MODEL] loaded ! Unblockinb all workers ..")
            self._ready_event.set()  # unblocksall waiting workers simultaneously 
        loader = threading.Thread(target = _load, daemon = True, name = "ModelLoader")
        loader.start()

    def moderate_content(self, content : str, worker_id : int ) -> str :
        """
        Waits for model, then moderates content with GPU slot limiting.

        FLOW:
        1. _ready_event.wait()         → block until model is loaded
        2. _inference_semaphore (2.5)  → max 3 concurrent GPU inferences
        3. self._model(content)        → actual inference

        Why Semaphore for GPU slots? GPU has limited parallel capacity.
        Running >3 inferences simultaneously causes OOM or slowdown.
        Semaphore enforces the limit cleanly.
        """
        # wait for model (all workers block here until model loads)
        self._ready_event.wait()

        # acquire GPU slot (at most 3 concurrent)
        with self._inference_semaphore:
            print(f" [MODEL] Worker - {worker_id} : running inference")
            print(f" GPU Slots in use : {3 - self._inference_semaphore._value}")
            time.sleep(0.1) # simulate GPU inference time 
            return self._model(content)

def run_content_moderation_system():
    """
    Use case : Youtube scale video comment moderation.
    Thousands of comments arrive in batches.This pattern handles model loading + bounded GPU parallelism cleanly.

    """      
    print("\n [EVENT] starting content moderation system")
    server = ModelServer() # modelserver 
    server.load_model_in_background()

    results = {}
    results_lock = threading.Lock()
    def worker(worker_id : int , content : str) :
        verdict = server.moderate_content(content, worker_id)
        with results_lock : 
            results[worker_id] = verdict 
        contents = [
                "Great video! Really helpful tutorial.",
                "This is spam spam spam buy now click here discount code",
                "I disagree with your analysis of the situation",
                "Subscribe and like for more content!",
                "Short",
                "A much longer comment that discusses many things in great detail and definitely exceeds fifty characters",
            ]
        threads = [
            threading.Thread(target = worker , args=(i,c)) for i,c in enumerate(contents)
        ]
        for t in threads : t.start()
        for t in threads : t.join()

        print(f"\n [EVENT] moderation results")
        for wid, verdict  in results.items():
            status = "FLAGGED " if verdict == "FLAGGED" else "SAFE"
            print(f"Worker -{wid} : {status} - {content[wid][:40]}...")


# Condition - producer / consumer batch coordination

class LLMBatchQueue:
    """
    A batch queue that accumulates requests and notifies when a batch is ready.

    REAL USE CASE: A high-throughput embedding service. Single embeddings
    cost the same API call as a batch of 100. Group individual requests
    into batches to maximize efficiency.

    Producer: adds individual texts to the queue
    Consumer: waits until batch is full OR timeout, then processes

    threading.Condition wraps a Lock but adds:
    - condition.wait(): releases lock and blocks until notified
    - condition.notify(): wakes ONE waiting thread
    - condition.notify_all(): wakes ALL waiting threads

    This allows "smart waiting" on a condition, not just mutual exclusion.
    """

    def __init__(self, batch_size: int = 5, timeout: float = 2.0):
        self._condition = threading.Condition()
        self._queue: list[tuple[int, str]] = []
        self._batch_size = batch_size
        self._timeout = timeout
        self._results: dict[int, list[float]] = {}
        self._request_counter = 0
        self._closed = False

    def submit(self, text: str) -> int:
        """
        Thread-safe: adds a text to the batch queue.
        Returns a request ID for result retrieval.
        """
        with self._condition:
            req_id = self._request_counter
            self._request_counter += 1
            self._queue.append((req_id, text))

            if len(self._queue) >= self._batch_size:
                self._condition.notify()  # Wake up batch processor

            return req_id

    def process_batches(self):
        """
        Runs in a dedicated thread. Waits for batches and processes them.

        condition.wait(timeout=2.0) means:
        - Wait up to 2 seconds for a notify() signal
        - If batch_size reached: process immediately (notified by submit())
        - If timeout: process whatever's in queue (prevents starvation)
        """
        print("  [BATCH] Batch processor started")
        while not self._closed:
            with self._condition:
                # Wait until batch is full OR timeout
                self._condition.wait_for(
                    lambda: len(self._queue) >= self._batch_size or self._closed,
                    timeout=self._timeout
                )
                batch = self._queue[:self._batch_size]
                self._queue = self._queue[self._batch_size:]

            if not batch:
                continue

            # Process the batch (simulate embedding API call)
            req_ids = [r[0] for r in batch]
            texts   = [r[1] for r in batch]
            print(f"  [BATCH] Processing batch of {len(batch)} texts: IDs {req_ids}")
            time.sleep(0.2)  # One API call for the entire batch!

            with self._condition:
                for req_id, text in batch:
                    self._results[req_id] = [hash(text) % 100 * 0.01] * 1536
                self._condition.notify_all()  # Wake up anyone waiting for results

    def get_result(self, req_id: int, timeout: float = 10.0) -> list[float]:
        """Waits until the result for req_id is available."""
        deadline = time.monotonic() + timeout
        with self._condition:
            while req_id not in self._results:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"Result for {req_id} not ready")
                self._condition.wait(timeout=remaining)
            return self._results.pop(req_id)

    def close(self):
        with self._condition:
            self._closed = True
            self._condition.notify_all()

# threadpooling - parallel image generation

@dataclass
class ImageGenRequest:
    prompt : str 
    style : str
    width : int = 1024 
    height : int = 1024

@dataclass
class GeneratedImage:
    request_id : str
    prompt : str
    file_path : str 
    generation_time_ms : float 
    thread_name : str


def generate_image(req : ImageGenRequest) -> GeneratedImage : 
    """
        Generates an image using a blocking image generation API.
    
        REAL USE CASE: An AI marketing platform that generates 50 product
        images simultaneously. The API is blocking (no async support).
        ThreadPoolExecutor handles all 50 in ~the time of 1 sequential call.
    
        This is the ideal ThreadPoolExecutor use case:
        - Blocking I/O (HTTP call to image gen service)
        - GIL released during the C-level network I/O
        - No shared state issues (each call is independent)
    
        In production with DALL-E:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"prompt": req.prompt, "n": 1, "size": f"{req.width}x{req.height}"}
            )
            url = response.json()["data"][0]["url"]
    """
    start = time.perf_counter()

    # simulates blocking HTTP call to DALLE / stable Diffusion API 
    time.sleep(random.uniform(1.0,3.0))

    elapsed = (time.perf_counter() - start ) * 1000
    req_id = f"img_{hash(req.prompt) % 10000:04d}"
    file_path = f"/output/{req_id}_{req.style}.png"

    return GeneratedImage(
        request_id= req_id,
        prompt = req.prompt,
        file_path = file_path,
        generation_time_ms= elapsed,
        thread_name= threading.current_thread().name
    )


def run_parallel_image_generation():
    """
    REAL USE CASE: Generating a full product catalog with AI images.
    50 products, each needing 3 style variants = 150 images.
    Sequential: 150 × 2s avg = 300 seconds (5 minutes)
    With ThreadPoolExecutor(10): ~30 seconds

    as_completed() lets you process images as they finish
    (real-time progress bar), not in submission order.
    """
    requests = [
        ImageGenRequest(f"Professional photo of {product}", style)
        for product in ["laptop", "headphones", "smartwatch", "keyboard"]
        for style in ["studio", "lifestyle", "minimal"]
    ]

    print(f"\n[THREAD_POOL] Generating {len(requests)} images with 5 workers...")
    generated = []
    failed = []
    t_start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=5, thread_name_prefix="imggen") as pool:
        # Submit all jobs immediately
        future_to_req = {
            pool.submit(generate_image, req): req
            for req in requests
        }

        # Process results as they complete (not in order)
        for future in as_completed(future_to_req):
            req = future_to_req[future]
            try:
                img = future.result(timeout=30)
                generated.append(img)
                print(f"  ✅ [{img.thread_name}] {img.file_path} ({img.generation_time_ms:.0f}ms)")
            except Exception as e:
                failed.append({"prompt": req.prompt, "error": str(e)})
                print(f"  ❌ Failed: {req.prompt[:30]} — {e}")

    total = (time.perf_counter() - t_start) * 1000
    print(f"\n[THREAD_POOL] Generated {len(generated)}/{len(requests)} images "
            f"in {total:.0f}ms")
    print(f"[THREAD_POOL] Sequential estimate: "
            f"~{len(requests) * 2000:.0f}ms ({len(requests) * 2:.0f}s)")

# Thread local storage - per-thread model instances


_thread_local = threading.local()


def get_embedding_model():
    """
    Returns THIS thread's own sentence transformer model.

    REAL USE CASE: A document indexing service where 8 threads each
    run sentence-transformer inference. The model is NOT thread-safe
    (internal buffers can corrupt if shared). Each thread needs its own.

    threading.local() provides a namespace where:
        - thread_local.model in Thread-1 ≠ thread_local.model in Thread-2
        - Each thread sees only ITS OWN attributes
        - Initialised lazily (first use per thread)

    This avoids:
        ❌ Global model = race conditions on internal state
        ❌ Lock around model = serial execution (defeats threading)
        ✅ Thread-local model = parallel, safe, one model per thread
    """
    if not hasattr(_thread_local, "model"):
        thread_name = threading.current_thread().name
        print(f"  [THREAD_LOCAL] {thread_name}: initializing model (first use)")
        # from sentence_transformers import SentenceTransformer
        # _thread_local.model = SentenceTransformer("all-MiniLM-L6-v2")
        time.sleep(0.3)  # Simulates model load
        _thread_local.model = lambda text: [hash(c) % 100 * 0.01 for c in text[:768]]

    return _thread_local.model


def embed_documents_threaded(texts: list[str]) -> dict[int, list[float]]:
    """
    Embeds documents in parallel using thread-local model instances.

    Each thread loads its own model ONCE (on first use), then reuses it
    for all subsequent documents assigned to that thread.
    """
    results = {}
    results_lock = threading.Lock()

    def embed_worker(idx: int, text: str):
        model = get_embedding_model()  # Gets THIS thread's model
        embedding = model(text)
        with results_lock:
            results[idx] = embedding

    print(f"\n[THREAD_LOCAL] Embedding {len(texts)} docs with thread-local models...")
    with ThreadPoolExecutor(max_workers=4, thread_name_prefix="embedder") as pool:
        futures = [pool.submit(embed_worker, i, t) for i, t in enumerate(texts)]
        for f in futures:
            f.result()  # Wait for all

    print(f"[THREAD_LOCAL] Done. Each thread loaded model exactly once.")
    return results


def main():
    print("=" * 70)
    print("SECTION 2: THREADING FOR GENAI APPLICATIONS")
    print("=" * 70)

    # 2.1 GIL
    demonstrate_gil()

    # 2.2 Lock
    print("\n--- 2.2 Lock: Thread-safe API Budget Tracking ---")
    simulate_concurrent_llm_calls()

    # 2.4 Event + Semaphore
    print("\n--- 2.4 Event + Semaphore: Model Loading Gate ---")
    run_content_moderation_system()

    # 2.5 Condition
    print("\n--- 2.5 Condition: Batch Embedding Queue ---")
    batch_queue = LLMBatchQueue(batch_size=3, timeout=1.0)
    processor_thread = threading.Thread(
        target=batch_queue.process_batches, daemon=True, name="BatchProcessor"
    )
    processor_thread.start()

    texts = ["RAG overview", "Attention mechanism", "Diffusion models",
             "RLHF training", "Vector embeddings", "Tokenisation"]
    req_ids = [batch_queue.submit(t) for t in texts]
    print(f"  [BATCH] Submitted {len(req_ids)} requests: IDs {req_ids}")
    time.sleep(2.0)  # Let batches process
    batch_queue.close()

    # 2.6 ThreadPoolExecutor
    print("\n--- 2.6 ThreadPoolExecutor: Parallel Image Generation ---")
    run_parallel_image_generation()

    # 2.7 Thread-local
    print("\n--- 2.7 Thread-local: Per-thread Model Instances ---")
    docs = [f"Document about AI topic {i}" for i in range(8)]
    embeddings = embed_documents_threaded(docs)
    print(f"[THREAD_LOCAL] Got {len(embeddings)} embeddings")


if __name__ == "__main__":
    main()
