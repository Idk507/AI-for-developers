Topic: Reliability and failure handling | Time: 10–15 minutes
Consider this scenario:
An enterprise AI assistant uses an LLM to analyze customer requests. During processing, the assistant invokes three external tools: a document retrieval API, a customer database, and a reporting service.
The document retrieval API occasionally times out.
The customer database sometimes responds slowly.
The reporting service can create new records.
Interview question: How would you design the agent so that temporary failures do not unnecessarily terminate the workflow, while ensuring that retries cannot accidentally create duplicate records?
In your answer, consider which operations are safe to retry, how you would distinguish transient failures from permanent failures, and how you would observe repeated failures in production.
You should also explain how you would use structured logging and distributed tracing to identify which tool caused the failure.

Here’s how I’d design the agent for **reliability and safe failure handling** in that scenario:

---

### 1. Classify Operations by Retry Safety
- **Safe to retry**:  
  - *Document retrieval API* → idempotent, no side effects. If it times out, retrying is fine.  
  - *Customer database queries* → read‑only lookups are safe to retry, though with backoff to avoid overload.  
- **Not safe to retry blindly**:  
  - *Reporting service (creates new records)* → retries could cause duplicate entries. Needs deduplication or idempotency guarantees.

---

### 2. Distinguish Transient vs Permanent Failures
- **Transient failures**: timeouts, temporary network errors, rate limits. → Retry with exponential backoff and jitter.  
- **Permanent failures**: invalid request, schema mismatch, authorization errors. → Fail fast, surface error to workflow.  
- **Mechanism**: classify errors by type/code; only retry transient ones.

---

### 3. Prevent Duplicate Record Creation
- Use **idempotency keys**: when creating a record, attach a unique request ID. If retried, the service recognizes the same ID and avoids duplicates.  
- Alternatively, implement **deduplication checks** (e.g., query before insert).

---

### 4. Observe Failures in Production
- **Structured logging**:  
  - Log each tool call with fields: tool name, request ID, error type, retry count, latency.  
  - Makes it easy to filter logs by tool or error category.  
- **Distributed tracing**:  
  - Trace each workflow across services with a correlation ID.  
  - Lets you see where latency or failure occurred (retrieval API vs database vs reporting service).  
  - Useful for spotting repeated failures or bottlenecks.

---

### 5. Workflow Design Principles
- Wrap each tool call in a **retry policy** tuned to its safety:  
  - Retrieval API → retry aggressively.  
  - Database → retry with cautious backoff.  
  - Reporting service → retry only with idempotency key.  
- Use **circuit breakers**: if a tool fails repeatedly, stop retrying and return a graceful fallback.  
- Monitor **retry counts and error rates** to detect systemic issues.

---

✅ In short:  
- Retry only idempotent operations freely.  
- Use idempotency keys for record creation.  
- Classify transient vs permanent failures.  
- Use structured logs + distributed tracing to pinpoint which tool failed and why.  

