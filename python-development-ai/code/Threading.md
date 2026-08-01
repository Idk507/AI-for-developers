
Optimized tool selection## `threading.Thread()` Parameters

Here are the main parameters you can pass to `threading.Thread()`:

```python
threading.Thread(
    target=None,           # function/method to run
    args=(),               # positional arguments tuple
    kwargs={},             # keyword arguments dictionary
    name=None,             # thread name (for debugging)
    daemon=False           # if True, thread won't keep process alive
)
```

### Breaking it down:

| Parameter            | Purpose                                              | Example                                                     |
| -------------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| **`target`** | The function/method the thread will execute          | `target=_load` or `target=worker_function`              |
| **`args`**   | Tuple of positional arguments to pass to`target`   | `args=(thread_id, 10)` → calls `target(thread_id, 10)` |
| **`kwargs`** | Dictionary of keyword arguments to pass to`target` | `kwargs={'name': 'Alice', 'age': 30}`                     |
| **`name`**   | Readable name for the thread (useful in debugging)   | `name="ModelLoader"`                                      |
| **`daemon`** | If`True`, thread exits when main program exits     | `daemon=True` means "don't wait for me to finish"         |

### From your code example:

```python
loader = threading.Thread(target=_load, daemon=True, name="ModelLoader")
loader.start()
```

- `target=_load` → run the `_load` function
- `daemon=True` → this is a background thread
- `name="ModelLoader"` → just a label for debugging

---

## Common Threading Functions & Synchronization Primitives

### **1. Thread Creation & Control**

```python
threading.Thread(target, args)      # Create a new thread
thread.start()                       # Start the thread
thread.join()                        # Wait for thread to finish
thread.is_alive()                    # Check if thread is running
threading.current_thread()           # Get current thread object
threading.enumerate()                # List all active threads
```

### **2. Lock — Mutual Exclusion**

Used to protect shared data from race conditions.

```python
lock = threading.Lock()

with lock:  # Only one thread enters at a time
    shared_counter += 1  # Safe operation
```

**From your code:**

```python
with self._lock:
    if self._cost_usd + call_cost > self.monthly_budget:
        return False
    self._call_count += 1  # Thread-safe increment
```

### **3. RLock — Re-entrant Lock**

Same thread can acquire it multiple times (won't deadlock).

```python
rlock = threading.RLock()

def recursive_function():
    with rlock:
        print("Entered")
        recursive_function()  # Same thread can re-enter safely
```

**From your code:**

```python
self._rlock = threading.RLock()
# Allows log_stage() to call log_stage() on the same thread
```

### **4. Event — Signal/Gate Pattern**

Blocks threads until a signal is sent.

```python
event = threading.Event()

# In worker threads:
event.wait()  # Block until event.set() is called

# In main/loader thread:
event.set()   # Unblock ALL waiting threads at once
event.clear()  # Reset the gate (block future waiters again)
```

**From your code:**

```python
self._ready_event = threading.Event()
# Workers call: event.wait()  → block until model is ready
# Loader calls: event.set()   → unblock all workers
```

### **5. Semaphore — Limited Permits**

Allows only N threads to proceed at once.

```python
sem = threading.Semaphore(3)  # Only 3 threads at a time

with sem:  # Acquire a permit
    do_inference()
    # When exiting, automatically releases permit for next thread
```

**From your code:**

```python
self._inference_semaphore = threading.Semaphore(3)
# Max 3 concurrent inferences
# If 10 threads try to enter, first 3 proceed, rest wait
```

### **6. Condition — Producer/Consumer**

Combines lock + signaling for complex synchronization.

```python
cond = threading.Condition()

# Consumer waits for data:
with cond:
    cond.wait()  # Wait for signal (releases lock while waiting)
    process_data()

# Producer adds data:
with cond:
    add_to_queue()
    cond.notify_all()  # Wake all waiters
```

### **7. Barrier — Wait for N Threads**

Makes N threads wait until all N reach a point.

```python
barrier = threading.Barrier(5)  # Wait for 5 threads

barrier.wait()  # Each thread blocks here
# When 5th thread reaches, all 5 unblock simultaneously
```

### **8. Timer — Delayed Execution**

Run a function after a delay (in a separate thread).

```python
timer = threading.Timer(2.0, callback_function, args=(arg1,))
timer.start()   # Start timer
timer.cancel()  # Cancel before it fires
```

---

## Quick Reference Table

| Object              | Purpose                      | Key Method                    |
| ------------------- | ---------------------------- | ----------------------------- |
| **Thread**    | Run code in parallel         | `start()`, `join()`       |
| **Lock**      | Only 1 thread at a time      | `acquire()` / `release()` |
| **RLock**     | Same thread can re-enter     | Same as Lock                  |
| **Event**     | All waiters unblock together | `set()`, `wait()`         |
| **Semaphore** | N threads max at a time      | `acquire()` / `release()` |
| **Condition** | Wait for signal + lock       | `wait()`, `notify()`      |
| **Barrier**   | Sync N threads at point      | `wait()`                    |

---

## Real-World Pattern from Your Code

```python
# 1. Create Event and Semaphore in __init__
self._ready_event = threading.Event()        # "gate" for workers
self._inference_semaphore = threading.Semaphore(3)  # "slots" for inference

# 2. Start loader in background thread
loader = threading.Thread(target=_load, daemon=True)
loader.start()

# 3. Workers wait for model, then take a semaphore slot
def worker():
    self._ready_event.wait()      # ← Block until model ready
    with self._inference_semaphore:  # ← Take a slot (max 3 at once)
        do_inference()
```

This prevents 100 threads from hammering your GPU at once—only 3 will run inference concurrently.Autopilot continued: The explanation of all the modules and functions of the Threading library is missing; only the parameters of `threading.Thread()` are provided.## Complete Threading Module Reference

Let me expand with a comprehensive guide to all major threading modules and functions:

---

## **threading Module — All Key Classes & Functions**

### **A. Thread Management**

```python
# Create and manage threads
threading.Thread(target, args, kwargs, name, daemon)
thread.start()                    # Begin execution
thread.join(timeout=None)         # Wait for thread to finish
thread.is_alive()                 # Returns True if running
thread.name                        # Get/set thread name
thread.ident                       # Thread ID (unique number)
thread.daemon                      # Get/set daemon status

threading.current_thread()         # Get the current thread object
threading.enumerate()              # List all active Thread objects
threading.active_count()           # Count of active threads
threading.get_ident()              # Get current thread ID
```

**Example:**

```python
threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
for t in threads:
    t.start()

for t in threads:
    t.join()  # Wait for ALL threads to complete

print(f"Active threads: {threading.active_count()}")
```

---

### **B. Locks & Mutual Exclusion**

#### **Lock** — Basic mutual exclusion

```python
lock = threading.Lock()

# Method 1: with statement (recommended)
with lock:
    # Only one thread executes this block
    shared_counter += 1

# Method 2: manual acquire/release
lock.acquire()
try:
    shared_counter += 1
finally:
    lock.release()

# Method 3: with timeout
acquired = lock.acquire(timeout=2.0)  # Wait max 2 seconds
if acquired:
    try:
        shared_counter += 1
    finally:
        lock.release()
```

#### **RLock** — Re-entrant Lock (same thread can re-acquire)

```python
rlock = threading.RLock()

def outer():
    with rlock:
        print("Outer locked")
        inner()  # Same thread, re-enters safely

def inner():
    with rlock:  # Does NOT deadlock
        print("Inner locked")

outer()
```

---

### **C. Event Synchronization**

#### **Event** — Wait for a signal

```python
event = threading.Event()

# Thread 1 (waiter)
event.wait()           # Blocks until set() is called
event.wait(timeout=5)  # Wait max 5 seconds

# Thread 2 (signaler)
event.set()            # Wake all waiters
event.clear()          # Reset; future waiters will block again
event.is_set()         # Check if event is set
```

**Real scenario:**

```python
startup_event = threading.Event()

def worker():
    print("Worker waiting for startup...")
    startup_event.wait()  # Blocks here
    print("Worker proceeding!")

t = threading.Thread(target=worker)
t.start()

time.sleep(2)
print("Main: starting now")
startup_event.set()  # Unblock worker

# Output:
# Worker waiting for startup...
# Main: starting now
# Worker proceeding!
```

---

### **D. Semaphore — Limited Resource Access**

#### **Semaphore** — N concurrent threads max

```python
sem = threading.Semaphore(3)  # Allow max 3 threads

with sem:
    # Only 3 threads execute this block at once
    # 4th+ threads wait until one of the first 3 exits
    do_work()
```

#### **BoundedSemaphore** — Safer version (prevents over-release)

```python
bsem = threading.BoundedSemaphore(2)

# This raises error if you release() more times than initialized
bsem.release()
bsem.release()
bsem.release()  # ❌ ValueError: Semaphore released too many times
```

**Real scenario — GPU inference pool:**

```python
gpu_slots = threading.Semaphore(3)  # Only 3 models can run inference at once

def inference_worker(request_id):
    with gpu_slots:  # Wait for free slot
        print(f"Request {request_id} running inference...")
        time.sleep(2)  # Simulate inference
        print(f"Request {request_id} done!")

threads = [threading.Thread(target=inference_worker, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Output: Only 3 inferences run at once, rest queue up
```

---

### **E. Condition — Producer/Consumer**

#### **Condition** — Lock + signaling combined

```python
condition = threading.Condition()

# Producer thread
def producer():
    with condition:
        queue.append(item)
        condition.notify_all()  # Wake all waiting consumers

# Consumer thread
def consumer():
    with condition:
        condition.wait()  # Wait and release lock
        item = queue.pop()  # Now safe to access queue
```

**Real scenario — Batch processing:**

```python
condition = threading.Condition()
batch = []
BATCH_SIZE = 5

def producer(item_id):
    global batch
    with condition:
        batch.append(item_id)
        if len(batch) == BATCH_SIZE:
            condition.notify_all()  # Batch is full, wake consumers

def consumer(worker_id):
    global batch
    while True:
        with condition:
            condition.wait()  # Wait for batch to fill
            if len(batch) >= BATCH_SIZE:
                items = batch[:BATCH_SIZE]
                batch = batch[BATCH_SIZE:]
                print(f"Worker {worker_id} processing: {items}")

# Start threads
prod_threads = [threading.Thread(target=producer, args=(i,)) for i in range(20)]
cons_threads = [threading.Thread(target=consumer, args=(i,)) for i in range(3)]
```

---

### **F. Barrier — Sync Multiple Threads**

```python
barrier = threading.Barrier(3)  # Wait for exactly 3 threads

def worker(worker_id):
    print(f"Worker {worker_id} starting phase 1")
    barrier.wait()  # Block until 3 threads reach here
    print(f"Worker {worker_id} phase 2 after sync")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# All 3 print "phase 1", then all 3 print "phase 2" together
```

---

### **G. Timer — Delayed Execution**

```python
timer = threading.Timer(2.0, callback, args=(arg1, arg2))
timer.start()    # Wait 2 seconds, then call callback in a thread
timer.cancel()   # Cancel timer before it fires

# Example: Timeout handler
def on_timeout():
    print("Request timed out!")

timeout = threading.Timer(5.0, on_timeout)
timeout.start()
result = slow_api_call()  # If this takes > 5 seconds
timeout.cancel()  # Cancel timeout if we got result in time
```

---

### **H. Local Thread Storage**

```python
local = threading.local()

def worker(worker_id):
    local.value = worker_id  # Each thread has its own 'value'
    print(f"Thread {worker_id} stored: {local.value}")
    time.sleep(1)
    print(f"Thread {worker_id} retrieved: {local.value}")  # Still there!

threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Each thread sees only its own stored value
```

**Real use case — Per-thread model instances:**

```python
model_local = threading.local()

def inference_worker(request_id):
    # Each thread loads model once, reuses it
    if not hasattr(model_local, 'model'):
        model_local.model = load_expensive_model()
  
    result = model_local.model.predict(data)
    return result
```

---

### **I. Queue — Thread-Safe Data Structure**

```python
from queue import Queue

q = Queue(maxsize=10)

# Producer thread
q.put(item)           # Add item (blocks if full)
q.put_nowait(item)    # Add without blocking (raises if full)

# Consumer thread
item = q.get()        # Remove item (blocks if empty)
item = q.get_nowait() # Remove without blocking (raises if empty)

q.task_done()         # Mark item as processed
q.join()              # Wait until all items processed
q.qsize()             # Current queue size (approx)
q.empty()             # Check if empty
q.full()              # Check if full
```

**Real scenario — Worker pool:**

```python
from queue import Queue
import threading

task_queue = Queue()

def worker():
    while True:
        task = task_queue.get()
        if task is None:  # Sentinel value to stop
            break
        print(f"Processing: {task}")
        task_queue.task_done()

# Start 3 worker threads
threads = [threading.Thread(target=worker) for _ in range(3)]
for t in threads:
    t.start()

# Add tasks
for i in range(10):
    task_queue.put(f"Task {i}")

# Wait for all tasks to finish
task_queue.join()

# Stop workers
for _ in range(3):
    task_queue.put(None)  # Sentinel signal
for t in threads:
    t.join()
```

---

## **Summary Table — All Threading Primitives**

| Class/Function       | Purpose                 | Key Methods                                |
| -------------------- | ----------------------- | ------------------------------------------ |
| `Thread`           | Run code in parallel    | `start()`, `join()`, `is_alive()`    |
| `Lock`             | Mutex (one thread only) | `acquire()`, `release()`               |
| `RLock`            | Re-entrant mutex        | Same as Lock                               |
| `Event`            | Signal all waiters      | `set()`, `wait()`, `clear()`         |
| `Semaphore`        | N threads max           | `acquire()`, `release()`               |
| `BoundedSemaphore` | Safer semaphore         | Same as Semaphore                          |
| `Condition`        | Lock + signal           | `wait()`, `notify()`, `notify_all()` |
| `Barrier`          | Sync N threads at point | `wait()`, `reset()`                    |
| `Timer`            | Delayed function call   | `start()`, `cancel()`                  |
| `local()`          | Thread-local storage    | Set/get per-thread vars                    |
| `Queue`            | Thread-safe queue       | `put()`, `get()`, `join()`           |

---

## **Decision Tree — Which to Use?**

```
Need to run code in parallel?
├─ YES → threading.Thread()

Need to protect shared data?
├─ Single thread re-enters?
│  └─ YES → RLock
│  └─ NO → Lock
│
Need to wait for an event?
├─ All threads wait for ONE signal?
│  └─ YES → Event
│  └─ NO → Condition (if producer/consumer)
│
Need to limit concurrent access?
├─ YES → Semaphore(N)

Need to sync N threads at a point?
├─ YES → Barrier(N)

Need delayed execution?
├─ YES → Timer(delay, callback)

Need per-thread storage?
├─ YES → threading.local()

Need thread-safe queue?
├─ YES → queue.Queue()
```

This completes a full reference to the threading module's functions and classes!
