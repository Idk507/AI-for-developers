# System Design Roadmap: Beginner to Advanced

## How to Use This Roadmap
Spend roughly 2–4 weeks per phase depending on your pace. Don't just read — build small proofs of concept, draw diagrams, and practice explaining designs out loud. System design is learned by doing and discussing, not memorizing.

---

## Phase 0: Prerequisites (1–2 weeks)
Before diving in, be comfortable with:
- **Programming fundamentals**: at least one language well (data structures, OOP basics)
- **Basic networking**: what happens when you type a URL into a browser
- **Basic OS concepts**: processes, threads, memory, disk vs RAM
- **A bit of database experience**: writing SQL queries, basic schema design

If any of these are shaky, spend a week solidifying them first — the rest of the roadmap builds on them.

---

## Phase 1: Foundations (Beginner)

### 1.1 Networking Basics
- Client-server model
- DNS resolution
- HTTP/HTTPS, request/response lifecycle
- TCP vs UDP
- REST APIs basics

### 1.2 How Computers Talk to Each Other
- IP addresses, ports
- Load balancers (what/why, L4 vs L7)
- Latency vs bandwidth
- CDNs — what they are and why they matter

### 1.3 Databases 101
- SQL vs NoSQL — when to use which
- Indexes and how they speed up queries
- Primary/foreign keys, normalization basics
- ACID properties

### 1.4 Basic System Components
- Web servers vs application servers
- What a cache is and why it helps
- What a queue/message broker does
- Vertical vs horizontal scaling

**Milestone project:** Design a simple URL shortener (like bit.ly) on paper — client, server, database, basic scaling.

---

## Phase 2: Core Building Blocks (Intermediate)

### 2.1 Scalability Fundamentals
- Horizontal vs vertical scaling trade-offs
- Stateless vs stateful services
- Load balancing algorithms (round robin, least connections, consistent hashing)
- Auto-scaling concepts

### 2.2 Databases in Depth
- SQL scaling: read replicas, sharding, partitioning
- NoSQL types: key-value, document, column-family, graph — and when each fits
- Indexing strategies (B-trees, hash indexes)
- Denormalization trade-offs

### 2.3 Caching
- Cache-aside, write-through, write-back strategies
- Cache eviction policies (LRU, LFU)
- Where to cache: client, CDN, server, database
- Cache invalidation challenges ("the two hard problems in CS")

### 2.4 Consistency & CAP Theorem
- CAP theorem (Consistency, Availability, Partition tolerance)
- Strong vs eventual consistency
- Read-your-writes, causal consistency
- Quorum-based consistency (reads/writes)

### 2.5 Asynchronous Processing
- Message queues (SQS, RabbitMQ) vs pub-sub (Kafka, SNS)
- When to go async vs sync
- Idempotency and retry mechanisms
- Dead-letter queues

### 2.6 API Design
- REST best practices, versioning
- Pagination, rate limiting
- gRPC vs REST vs GraphQL — trade-offs
- Designing for backward compatibility

**Milestone project:** Design a rate limiter, then design an e-commerce product catalog system with caching and search.

---

## Phase 3: Distributed Systems Concepts (Advanced Intermediate)

### 3.1 Data Partitioning & Sharding
- Hash-based, range-based, directory-based sharding
- Consistent hashing (deep dive — used everywhere)
- Rebalancing shards, hot partitions

### 3.2 Replication
- Leader-follower (master-slave) replication
- Multi-leader and leaderless replication
- Synchronous vs asynchronous replication
- Conflict resolution (vector clocks, CRDTs)

### 3.3 Consensus & Coordination
- Why consensus is hard (split brain, network partitions)
- Paxos and Raft (at least conceptually)
- Leader election
- Distributed locks (and why they're tricky)
- Zookeeper/etcd — what problems they solve

### 3.4 Fault Tolerance & Reliability
- Failure detection (heartbeats, timeouts)
- Redundancy and replication for availability
- Circuit breakers, bulkheads, retries with backoff
- Graceful degradation
- Chaos engineering basics

### 3.5 Communication Patterns
- Synchronous vs asynchronous communication
- Service discovery
- API gateways
- Sidecars and service mesh (Envoy, Istio) — conceptual understanding

### 3.6 Storage Systems Deep Dive
- Distributed file systems (HDFS concepts)
- Object storage (S3-like systems)
- Time-series databases
- Search systems (inverted indexes, Elasticsearch basics)

**Milestone project:** Design a distributed cache (like Redis Cluster), then design a chat application (like WhatsApp) with online presence and message delivery guarantees.

---

## Phase 4: Large-Scale System Design (Advanced)

Practice designing these end-to-end, focusing on trade-offs, not just "correct" answers:

### 4.1 Classic Practice Problems
- URL shortener (revisit with full scale considerations)
- Rate limiter (distributed version)
- Web crawler
- News feed / social media timeline (like Twitter/Instagram feed)
- Chat system (WhatsApp/Messenger)
- Video streaming platform (YouTube/Netflix)
- Ride-sharing system (Uber/Lyft)
- Ticket booking system (BookMyShow/Ticketmaster) — handling concurrency/inventory
- Distributed key-value store (DynamoDB-like)
- Notification system
- Search autocomplete / typeahead
- Payment system (idempotency, double-spend prevention)
- File storage/sync system (Dropbox/Google Drive)

### 4.2 Deep Specialization Topics
- Geospatial indexing (quad trees, geohashing) — for location-based apps
- Recommendation systems at scale
- Real-time analytics pipelines (Kafka + Flink/Spark Streaming)
- Multi-region / global system design (data residency, latency, disaster recovery)
- Event sourcing and CQRS patterns
- Rate limiting at global scale (token bucket, sliding window across regions)

### 4.3 Non-Functional Requirements Mastery
- Estimating scale: back-of-envelope calculations (QPS, storage, bandwidth)
- Designing for 99.9% vs 99.99% availability — what changes
- Security considerations (authentication, authorization, encryption at rest/in transit)
- Cost optimization at scale
- Observability: logging, metrics, tracing (Prometheus, Grafana, distributed tracing)

---

## Phase 5: Mastery & Interview-Readiness

### 5.1 The System Design Framework
Practice a repeatable approach for any problem:
1. Clarify requirements (functional + non-functional)
2. Estimate scale (back-of-envelope math)
3. Define API/interface
4. High-level design (draw boxes and arrows)
5. Deep dive into critical components
6. Address bottlenecks, trade-offs, and failure scenarios
7. Discuss monitoring and future scaling

### 5.2 Study Real-World Architectures
Read engineering blogs from companies at scale:
- Netflix Tech Blog, Uber Engineering, Airbnb Engineering, Discord Engineering, Meta Engineering
- Look at case studies of real outages (postmortems) to learn failure patterns

### 5.3 Practice Actively
- Do mock interviews (with peers or platforms)
- Explain designs out loud, on a whiteboard/paper — this reveals gaps fast
- Get feedback and iterate on the same problem multiple times with added constraints (e.g., "now design it for 10x traffic")

### 5.4 Build Something Real
- Implement a mini version of one of these systems (e.g., a basic distributed cache or a simplified message queue) to internalize concepts beyond theory

---

## Recommended Resources

**Books:**
- *Designing Data-Intensive Applications* by Martin Kleppmann (the single best resource — read this thoroughly)
- *System Design Interview* Vol 1 & 2 by Alex Xu
- *Database Internals* by Alex Petrov (for deeper database mechanics)

**Free Online:**
- High Scalability blog
- ByteByteGo (newsletter and YouTube)
- Engineering blogs mentioned above

**Practice Platforms:**
- Excalidraw or draw.io for diagramming practice
- Mock interview platforms (Pramp, interviewing.io)

---

## Suggested Timeline (Full-Time Focus)

| Phase | Duration |
|---|---|
| Phase 0: Prerequisites | 1–2 weeks |
| Phase 1: Foundations | 2–3 weeks |
| Phase 2: Core Building Blocks | 3–4 weeks |
| Phase 3: Distributed Systems | 4–6 weeks |
| Phase 4: Large-Scale Design Practice | 6–8 weeks |
| Phase 5: Mastery & Interview Prep | Ongoing |

**Total: roughly 4–6 months** of consistent study for solid depth, longer if going part-time alongside a job.

---

