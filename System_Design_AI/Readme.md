# AI / GenAI System Design Roadmap: Beginner to Advanced

This assumes you already have (or are building) the classical system design foundation from the general roadmap. AI system design layers ML/LLM-specific concerns — data pipelines, model serving, vector search, prompt/context management — on top of those same distributed systems fundamentals.

---

## Phase 0: Prerequisites (2–3 weeks)

- Solid classical system design (caching, load balancing, databases, queues — see general roadmap)
- Basic ML concepts: what training vs inference means, what a model checkpoint is, overfitting/generalization
- Basic understanding of neural networks (you don't need to derive backprop, but know what a forward pass is)
- Familiarity with Python and at least one ML framework (PyTorch or similar) at a conceptual level
- Basic understanding of what an LLM is: tokens, context window, embeddings, autoregressive generation

---

## Phase 1: Foundations of ML/AI Systems (Beginner)

### 1.1 The ML System Lifecycle
- Data collection → training → evaluation → deployment → monitoring → retraining loop
- Batch vs online (real-time) inference
- Offline evaluation vs online (A/B testing) evaluation

### 1.2 Core AI-Specific Concepts
- Embeddings: what they are, how similarity search works (cosine similarity, dot product)
- Tokenization basics (BPE, tokenizers) and why token count matters for cost/latency
- Context window and its practical limits
- Model quantization basics (FP32 → FP16 → INT8) and why it matters for serving

### 1.3 Basic GenAI Application Architecture
- Prompt → Model API → Response, the simplest possible pipeline
- API-based models (calling a hosted LLM) vs self-hosted models
- Streaming responses (token-by-token) vs batch responses
- Basic prompt engineering as a system design lever (not just a writing skill)

**Milestone project:** Design a simple chatbot wrapper — API gateway, LLM call, basic conversation history storage.

---

## Phase 2: Core GenAI Application Patterns (Intermediate)

### 2.1 Retrieval-Augmented Generation (RAG)
- Why RAG exists: grounding, reducing hallucination, fresh/private data
- RAG pipeline: ingestion → chunking → embedding → storage → retrieval → augmentation → generation
- Chunking strategies (fixed-size, semantic, recursive) and their trade-offs
- Re-ranking retrieved results before passing to the LLM

### 2.2 Vector Databases & Search
- What a vector database does differently from a traditional DB
- Approximate Nearest Neighbor (ANN) search algorithms: HNSW, IVF, product quantization (conceptual level)
- Popular systems: Pinecone, Weaviate, Milvus, pgvector, FAISS — trade-offs (managed vs self-hosted, scale, cost)
- Hybrid search (keyword/BM25 + vector search combined)
- Metadata filtering alongside vector search

### 2.3 Prompt & Context Management
- System prompts vs user prompts vs few-shot examples
- Context window budgeting when combining system prompt + retrieved docs + chat history
- Prompt templates and versioning (treating prompts like code — version control, testing)
- Structured output (JSON mode, function calling / tool use)

### 2.4 Memory Systems for Conversational AI
- Short-term memory (conversation buffer within context window)
- Long-term memory (summarization, vector-stored memory, user profile stores)
- Sliding window vs summarization-based history compression

### 2.5 Cost & Latency Basics
- Token-based pricing models and how architecture choices affect cost
- Caching LLM responses (semantic caching — caching based on meaning, not exact match)
- Latency budget: network + retrieval + inference + generation

**Milestone project:** Design a RAG-based customer support assistant over a company's documentation, including ingestion pipeline and retrieval quality considerations.

---

## Phase 3: Model Serving & Inference Systems (Advanced Intermediate)

### 3.1 Model Serving Fundamentals
- Serving frameworks: vLLM, TensorRT-LLM, Triton Inference Server, TGI — what problems each solves
- Batching requests (dynamic/continuous batching) to maximize GPU utilization
- KV-cache management — why it's the key bottleneck in LLM serving memory
- Speculative decoding (using a small model to draft, large model to verify) for speed

### 3.2 GPU Infrastructure Basics
- Why GPUs, not CPUs, for inference (parallelism)
- Model parallelism vs data parallelism vs pipeline parallelism (conceptual)
- Multi-GPU and multi-node serving for large models
- Autoscaling GPU workloads (cold start problem is much worse than CPU services)

### 3.3 Multi-Model & Multi-Tenant Systems
- Serving multiple models/versions behind one gateway
- Model routing (routing simple queries to cheap/small models, complex ones to large models) — "model cascades"
- LoRA adapters: serving many fine-tuned variants efficiently on a shared base model
- Rate limiting and quota management per tenant/user in AI APIs

### 3.4 Fine-Tuning & Customization Systems
- Full fine-tuning vs parameter-efficient fine-tuning (LoRA, QLoRA) — infra implications
- RLHF / preference-tuning pipeline at a high level
- Data pipeline for fine-tuning: collection, labeling, quality filtering, deduplication
- Evaluation harnesses for fine-tuned models (regression testing against benchmarks)

### 3.5 Observability for AI Systems
- Logging prompts/responses (with privacy considerations)
- Tracing multi-step AI pipelines (especially agentic ones)
- Tracking hallucination rate, latency, token usage, cost per request
- Tools: LangSmith, Weights & Biases, Arize, custom eval pipelines

**Milestone project:** Design an LLM inference platform serving multiple fine-tuned models with autoscaling, routing, and cost tracking.

---

## Phase 4: Agentic & Multi-Component AI Systems (Advanced)

### 4.1 AI Agents
- Agent loop: perceive → plan → act → observe → repeat
- Tool use / function calling architecture
- Single-agent vs multi-agent systems (orchestrator + specialized sub-agents)
- Handling agent failures, infinite loops, and runaway costs (guardrails on iteration count)

### 4.2 Orchestration Frameworks (Conceptual Understanding)
- What frameworks like LangChain, LlamaIndex, or custom orchestrators actually solve
- Workflow/DAG-based orchestration vs free-form agent loops
- State management across multi-step agent workflows
- Human-in-the-loop checkpoints for high-stakes actions

### 4.3 Data Pipelines for GenAI at Scale
- Ingesting and continuously updating knowledge bases (incremental re-indexing)
- Handling document versioning and staleness in RAG systems
- Data deduplication and quality filtering at scale
- Multi-modal data pipelines (text, images, audio) if relevant to your use case

### 4.4 Safety, Guardrails & Reliability
- Input/output content filtering and moderation layers
- Prompt injection defenses (treating retrieved/user content as untrusted)
- PII detection and redaction in pipelines
- Fallback strategies when a model is unavailable or produces low-confidence output
- Circuit breakers for cascading agent failures

### 4.5 Evaluation at Scale
- Automated eval pipelines (LLM-as-judge, golden datasets, regression suites)
- Online evaluation: user feedback loops, thumbs up/down signal collection
- A/B testing prompts, models, and RAG configurations in production
- Handling non-determinism in evaluation (same prompt, different outputs)

**Milestone project:** Design a multi-agent research assistant that can browse, retrieve, summarize, and cite sources — with guardrails against runaway tool calls and cost blowups.

---

## Phase 5: Large-Scale, Production-Grade GenAI Systems (Mastery)

Practice designing these end-to-end:

- **AI coding assistant** (like Copilot/Cursor) — codebase indexing, context retrieval, low-latency completion, multi-file awareness
- **Enterprise RAG search platform** — permission-aware retrieval (users only see docs they're authorized for), freshness, multi-tenant isolation
- **Conversational AI at scale** (like ChatGPT/Claude.ai serving millions of users) — session management, streaming, rate limiting, model routing, abuse prevention
- **AI content moderation pipeline** — real-time classification at scale with human review escalation
- **Recommendation system powered by embeddings** — combining collaborative filtering with LLM-based re-ranking
- **Multi-modal AI pipeline** — image/video/audio understanding combined with text generation
- **Voice AI assistant** — speech-to-text, LLM processing, text-to-speech, with end-to-end latency budget under a few hundred ms
- **AI agent marketplace/platform** — serving many third-party agents with sandboxing, billing, and tool-permission systems

### 5.1 Advanced Non-Functional Concerns
- Global multi-region GenAI deployment (data residency for prompts/outputs, GPU availability per region)
- Cost optimization at massive scale (spot instances, model distillation, caching layers, cascade routing)
- Compliance considerations (data retention for training exclusion, audit logs, EU AI Act–style considerations)
- Handling model deprecation/migration without breaking downstream systems
- Disaster recovery when a foundation model provider has an outage (multi-provider fallback design)

### 5.2 The AI System Design Framework
A repeatable structure for interviews or real design work:
1. Clarify the AI task (generation, classification, retrieval, agentic) and success metrics
2. Define data sources and freshness requirements
3. Choose model strategy: API vs self-hosted, single model vs cascade, fine-tune vs prompt-only
4. Design the retrieval/context pipeline if applicable (RAG, memory, tools)
5. Design serving infra: batching, autoscaling, latency/cost targets
6. Add guardrails: safety, hallucination mitigation, fallback paths
7. Design evaluation and monitoring loops
8. Discuss cost, scaling, and failure modes

---

## Recommended Resources

**Foundational Reading:**
- *Designing Machine Learning Systems* by Chip Huyen — the best single book for this exact topic
- *Designing Data-Intensive Applications* by Martin Kleppmann — still essential, underlies everything
- Anthropic and OpenAI's own engineering/prompting documentation — practical, current best practices

**Blogs & Papers to Track:**
- Chip Huyen's blog (ML systems in production)
- Eugene Yan's blog (applied ML/LLM systems)
- Anthropic, OpenAI, Google DeepMind engineering blogs
- vLLM and Hugging Face blog posts on serving optimizations
- Papers: RAG (Lewis et al.), RLHF (InstructGPT paper), LoRA paper — for foundational understanding, not implementation depth

**Hands-On Practice:**
- Build a RAG pipeline from scratch (not just with a framework) to understand every moving part
- Deploy a small open-source LLM locally with vLLM or similar to understand serving mechanics
- Build a simple agent with tool use and deliberately break it (loops, bad tool calls) to learn failure handling

---

## Suggested Timeline (Full-Time Focus)

| Phase | Duration |
|---|---|
| Phase 0: Prerequisites | 2–3 weeks |
| Phase 1: Foundations | 2–3 weeks |
| Phase 2: Core GenAI Patterns (RAG, vector DBs) | 4–5 weeks |
| Phase 3: Model Serving & Inference | 5–6 weeks |
| Phase 4: Agentic Systems | 5–6 weeks |
| Phase 5: Mastery & Large-Scale Practice | Ongoing |

**Total: roughly 4–5 months** for solid depth, assuming the classical system design foundation is already in place.

---

## Key Mindset Shift
Classical system design optimizes for **correctness and consistency of data**. AI system design adds a layer where the "output" is probabilistic — the same request can produce different results, and correctness itself is fuzzy (Was the answer good? Was it grounded? Was it safe?). Mastery here means designing systems that manage that uncertainty deliberately: through retrieval grounding, evaluation loops, guardrails, and graceful fallback — not systems that pretend the model is a deterministic function.
