# Apache Kafka: Beginner to Advanced — Complete Guide

---

## PART 1: What is Kafka? (Beginner)

### The Problem Kafka Solves

Imagine a large e-commerce system. You have:
- An **order service** generating orders
- An **inventory service** that needs to update stock
- A **notification service** that sends emails
- An **analytics service** tracking revenue

Without Kafka, every service talks directly to every other service — creating a tangled web of dependencies. If one service goes down, everything breaks.

**Kafka is a distributed event streaming platform** that acts as a central nervous system — all services publish and consume events through it.

```
WITHOUT KAFKA                        WITH KAFKA
─────────────                        ──────────
Orders ──► Inventory                 Orders ──► [KAFKA] ──► Inventory
       ──► Notify                                      ──► Notify
       ──► Analytics                                   ──► Analytics
```

---

### Core Concepts (Mental Model)

Think of Kafka like a **newspaper publishing system**:

| Concept | Newspaper Analogy | Kafka |
|---|---|---|
| **Topic** | The newspaper section (Sports, Finance) | Named category/channel for events |
| **Producer** | The journalist writing articles | App that sends events |
| **Consumer** | The reader | App that reads events |
| **Broker** | The printing press / distribution center | Kafka server node |
| **Partition** | Different delivery routes | Sub-division of a topic for parallelism |
| **Offset** | Page number in the newspaper | Position of a message in a partition |
| **Consumer Group** | A team of readers splitting sections | Group of consumers sharing the load |

---

## PART 2: Kafka Architecture (Intermediate)

```
┌──────────────────────────────────────────────────────────────────┐
│                        KAFKA CLUSTER                             │
│                                                                  │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                       │
│  │ Broker 1│   │ Broker 2│   │ Broker 3│   ← Broker = Server   │
│  │         │   │         │   │         │                        │
│  │Topic: A │   │Topic: A │   │Topic: B │                        │
│  │Part 0   │   │Part 1   │   │Part 0   │                        │
│  │[Leader] │   │[Leader] │   │[Leader] │                        │
│  │         │   │         │   │         │                        │
│  └─────────┘   └─────────┘   └─────────┘                        │
│                                                                  │
│  ┌──────────────┐   ZooKeeper / KRaft                           │
│  │  Controller  │   (Cluster metadata & leader election)         │
│  └──────────────┘                                               │
└──────────────────────────────────────────────────────────────────┘
        ▲                              │
    Producers                      Consumers
  (write events)                (read events)
```

### Topics & Partitions Deep Dive

```
Topic: "user-events"
│
├── Partition 0:  [msg0] [msg1] [msg4] [msg7]  ← offset 0,1,2,3
├── Partition 1:  [msg2] [msg5] [msg8]          ← offset 0,1,2
└── Partition 2:  [msg3] [msg6] [msg9]          ← offset 0,1,2
```

- Messages within a partition are **strictly ordered**
- Messages across partitions are **NOT ordered**
- More partitions = more **parallelism** = higher throughput
- Each partition has one **Leader** broker and multiple **Replica** brokers

### Replication — Fault Tolerance

```
Topic "orders", Partition 0, Replication Factor = 3

Broker 1 [LEADER]  ◄── Producers write here
Broker 2 [REPLICA] ◄── Synced copy
Broker 3 [REPLICA] ◄── Synced copy

If Broker 1 dies → Broker 2 becomes the new LEADER automatically
```

---

## PART 3: Kafka in Production

### Producer Configuration (Production-Grade)

```python
# producer_config.py
from confluent_kafka import Producer
import json, logging

producer_config = {
    # Connection
    'bootstrap.servers': 'kafka-broker-1:9092,kafka-broker-2:9092,kafka-broker-3:9092',

    # Reliability: wait for ALL in-sync replicas to acknowledge
    'acks': 'all',              # 0=fire-forget, 1=leader only, all=safest

    # Prevent duplicate messages on retry
    'enable.idempotence': True,

    # Retry settings
    'retries': 10,
    'retry.backoff.ms': 500,

    # Batching for throughput
    'linger.ms': 5,             # Wait 5ms to batch messages together
    'batch.size': 65536,        # 64KB batch size

    # Compression
    'compression.type': 'snappy',  # snappy/lz4/zstd/gzip

    # Serialization
    'key.serializer': 'org.apache.kafka.common.serialization.StringSerializer',

    # Security (Production)
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'your-api-key',
    'sasl.password': 'your-api-secret',
}

class KafkaProducerService:
    def __init__(self):
        self.producer = Producer(producer_config)
        self.logger = logging.getLogger(__name__)

    def publish(self, topic: str, key: str, value: dict):
        try:
            self.producer.produce(
                topic=topic,
                key=key.encode('utf-8'),
                value=json.dumps(value).encode('utf-8'),
                on_delivery=self._delivery_callback
            )
            self.producer.poll(0)  # Trigger delivery callbacks
        except Exception as e:
            self.logger.error(f"Failed to produce: {e}")
            raise

    def _delivery_callback(self, err, msg):
        if err:
            self.logger.error(f"Delivery failed: {err}")
        else:
            self.logger.info(
                f"Delivered to {msg.topic()} "
                f"[partition {msg.partition()}] "
                f"offset {msg.offset()}"
            )

    def flush(self):
        self.producer.flush(timeout=30)
```

### Consumer Configuration (Production-Grade)

```python
# consumer_config.py
from confluent_kafka import Consumer, KafkaError
import json, signal, logging

consumer_config = {
    'bootstrap.servers': 'kafka-broker-1:9092,kafka-broker-2:9092,kafka-broker-3:9092',
    'group.id': 'order-processing-service',

    # Where to start reading if no committed offset exists
    'auto.offset.reset': 'earliest',  # or 'latest'

    # IMPORTANT: Disable auto-commit for exactly-once semantics
    'enable.auto.commit': False,

    # Session timeout — if consumer doesn't heartbeat, it's considered dead
    'session.timeout.ms': 30000,
    'heartbeat.interval.ms': 10000,

    # Max records per poll
    'max.poll.records': 500,

    # Security
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'your-api-key',
    'sasl.password': 'your-api-secret',
}

class KafkaConsumerService:
    def __init__(self, topics: list):
        self.consumer = Consumer(consumer_config)
        self.consumer.subscribe(topics)
        self.running = True
        self.logger = logging.getLogger(__name__)
        signal.signal(signal.SIGTERM, self._shutdown)

    def consume(self, process_fn):
        try:
            while self.running:
                messages = self.consumer.consume(num_messages=100, timeout=1.0)

                for msg in messages:
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            continue  # End of partition, not an error
                        raise Exception(f"Consumer error: {msg.error()}")

                    try:
                        value = json.loads(msg.value().decode('utf-8'))
                        key = msg.key().decode('utf-8') if msg.key() else None

                        # Process the message
                        process_fn(key, value)

                        # Manually commit AFTER successful processing
                        self.consumer.commit(msg)

                    except Exception as e:
                        self.logger.error(f"Processing failed for offset "
                                          f"{msg.offset()}: {e}")
                        # Send to Dead Letter Queue
                        self._send_to_dlq(msg, str(e))

        finally:
            self.consumer.close()

    def _send_to_dlq(self, msg, error_reason):
        # Dead Letter Queue pattern for failed messages
        dlq_producer = KafkaProducerService()
        dlq_producer.publish(
            topic=f"{msg.topic()}.dlq",
            key=msg.key().decode('utf-8') if msg.key() else "unknown",
            value={
                "original_topic": msg.topic(),
                "original_partition": msg.partition(),
                "original_offset": msg.offset(),
                "error": error_reason,
                "payload": msg.value().decode('utf-8')
            }
        )

    def _shutdown(self, signum, frame):
        self.logger.info("Shutting down consumer...")
        self.running = False
```

---

## PART 4: Kafka + GenAI Applications

This is where Kafka becomes extremely powerful. GenAI systems have unique needs:
- LLM inference is **slow** (1–30 seconds per request)
- Requests need to be **queued and distributed**
- Results need to be **streamed back**
- RAG pipelines need **real-time document ingestion**
- AI agents need **event-driven coordination**

### Architecture: GenAI Event Pipeline

```
User Request
     │
     ▼
API Gateway ──► [ai-inference-requests] ──► LLM Worker Pool
                        TOPIC                   │
                                                ▼
                                         LLM Inference
                                         (GPT/Claude/Llama)
                                                │
                                                ▼
                              [ai-inference-results] ──► Response Handler
                                        TOPIC                   │
                                                                ▼
                                                         WebSocket/SSE
                                                         to User

RAG Pipeline:
Documents ──► [document-ingestion] ──► Chunker ──► [chunks] ──► Embedder
                                                                    │
                                                                    ▼
                                                              Vector DB
                                                           (Pinecone/Weaviate)
```

### Implementation: LLM Request Queue with Kafka

```python
# genai_kafka_pipeline.py
import asyncio
import uuid
import json
from confluent_kafka import Producer, Consumer
from anthropic import Anthropic
from dataclasses import dataclass, asdict
from typing import Optional
import redis  # For request tracking

@dataclass
class LLMRequest:
    request_id: str
    user_id: str
    prompt: str
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 1000
    system_prompt: Optional[str] = None
    metadata: dict = None

@dataclass
class LLMResponse:
    request_id: str
    user_id: str
    content: str
    model: str
    usage: dict
    status: str  # "success" | "error"
    error: Optional[str] = None

class GenAIKafkaPipeline:
    REQUESTS_TOPIC = "ai-inference-requests"
    RESPONSES_TOPIC = "ai-inference-responses"
    STREAMING_TOPIC = "ai-streaming-chunks"

    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': 'localhost:9092',
            'acks': 'all',
            'enable.idempotence': True,
        })
        self.anthropic = Anthropic()
        self.redis = redis.Redis(host='localhost', port=6379)

    # ── PRODUCER SIDE: Submit LLM request ─────────────────────
    def submit_request(self, user_id: str, prompt: str,
                       system_prompt: str = None) -> str:
        request_id = str(uuid.uuid4())

        request = LLMRequest(
            request_id=request_id,
            user_id=user_id,
            prompt=prompt,
            system_prompt=system_prompt
        )

        # Track request status in Redis
        self.redis.setex(
            f"llm:request:{request_id}",
            3600,  # 1 hour TTL
            json.dumps({"status": "queued", "user_id": user_id})
        )

        # Publish to Kafka
        self.producer.produce(
            topic=self.REQUESTS_TOPIC,
            key=user_id,  # Same user's requests go to same partition
            value=json.dumps(asdict(request)),
            on_delivery=self._delivery_callback
        )
        self.producer.flush()

        return request_id

    # ── CONSUMER SIDE: LLM Worker ─────────────────────────────
    def start_llm_worker(self, worker_id: str):
        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'llm-workers',      # Multiple workers share load
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
        })
        consumer.subscribe([self.REQUESTS_TOPIC])

        print(f"Worker {worker_id} started, waiting for requests...")

        while True:
            messages = consumer.consume(num_messages=1, timeout=1.0)

            for msg in messages:
                if msg.error():
                    continue

                request_data = json.loads(msg.value())
                request = LLMRequest(**request_data)

                print(f"Worker {worker_id} processing request {request.request_id}")

                # Update status
                self.redis.setex(
                    f"llm:request:{request.request_id}",
                    3600,
                    json.dumps({"status": "processing", "worker": worker_id})
                )

                # Call LLM
                response = self._call_llm(request)

                # Publish response
                self.producer.produce(
                    topic=self.RESPONSES_TOPIC,
                    key=request.user_id,
                    value=json.dumps(asdict(response))
                )
                self.producer.flush()

                # Commit offset
                consumer.commit(msg)

    def _call_llm(self, request: LLMRequest) -> LLMResponse:
        try:
            messages = [{"role": "user", "content": request.prompt}]
            kwargs = {
                "model": request.model,
                "max_tokens": request.max_tokens,
                "messages": messages
            }
            if request.system_prompt:
                kwargs["system"] = request.system_prompt

            response = self.anthropic.messages.create(**kwargs)

            return LLMResponse(
                request_id=request.request_id,
                user_id=request.user_id,
                content=response.content[0].text,
                model=request.model,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                status="success"
            )
        except Exception as e:
            return LLMResponse(
                request_id=request.request_id,
                user_id=request.user_id,
                content="",
                model=request.model,
                usage={},
                status="error",
                error=str(e)
            )

    def _delivery_callback(self, err, msg):
        if err:
            print(f"Delivery failed: {err}")
        else:
            print(f"Delivered to partition {msg.partition()}, offset {msg.offset()}")
```

### RAG Pipeline with Real-Time Document Ingestion

```python
# rag_kafka_pipeline.py
from sentence_transformers import SentenceTransformer
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGKafkaPipeline:
    INGESTION_TOPIC = "document-ingestion"
    CHUNKS_TOPIC = "document-chunks"
    EMBEDDINGS_TOPIC = "document-embeddings"

    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=64,
            separators=["\n\n", "\n", ". ", " "]
        )
        self.pinecone_index = pinecone.Index("rag-documents")

    # Stage 1: Ingest raw documents
    def ingest_document(self, doc_id: str, content: str,
                        metadata: dict):
        producer = KafkaProducerService()
        producer.publish(
            topic=self.INGESTION_TOPIC,
            key=doc_id,
            value={
                "doc_id": doc_id,
                "content": content,
                "metadata": metadata
            }
        )

    # Stage 2: Chunking worker
    def start_chunker_worker(self):
        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'doc-chunkers',
            'enable.auto.commit': False
        })
        consumer.subscribe([self.INGESTION_TOPIC])
        chunker_producer = KafkaProducerService()

        while True:
            messages = consumer.consume(num_messages=10, timeout=1.0)
            for msg in messages:
                doc = json.loads(msg.value())
                chunks = self.text_splitter.split_text(doc['content'])

                for i, chunk in enumerate(chunks):
                    chunker_producer.publish(
                        topic=self.CHUNKS_TOPIC,
                        key=f"{doc['doc_id']}-chunk-{i}",
                        value={
                            "doc_id": doc['doc_id'],
                            "chunk_id": f"{doc['doc_id']}-{i}",
                            "chunk_index": i,
                            "total_chunks": len(chunks),
                            "content": chunk,
                            "metadata": doc['metadata']
                        }
                    )
                consumer.commit(msg)

    # Stage 3: Embedding worker
    def start_embedding_worker(self):
        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'doc-embedders',
            'enable.auto.commit': False
        })
        consumer.subscribe([self.CHUNKS_TOPIC])

        while True:
            # Batch for efficiency
            messages = consumer.consume(num_messages=32, timeout=1.0)
            if not messages:
                continue

            batch_chunks = []
            batch_metadata = []

            for msg in messages:
                chunk = json.loads(msg.value())
                batch_chunks.append(chunk['content'])
                batch_metadata.append(chunk)

            # Batch embed
            embeddings = self.embedding_model.encode(
                batch_chunks,
                batch_size=32,
                show_progress_bar=False
            )

            # Upsert to Pinecone
            vectors = [
                (
                    chunk['chunk_id'],
                    embedding.tolist(),
                    {
                        "doc_id": chunk['doc_id'],
                        "content": chunk['content'][:1000],
                        **chunk['metadata']
                    }
                )
                for chunk, embedding in zip(batch_metadata, embeddings)
            ]
            self.pinecone_index.upsert(vectors=vectors)

            # Commit all
            for msg in messages:
                consumer.commit(msg)
            print(f"Embedded and stored {len(vectors)} chunks")
```

### AI Agent Coordination with Kafka

```python
# agent_orchestration.py
"""
Multi-Agent System using Kafka for coordination:

Agent Types:
  - Planner Agent: Breaks down tasks
  - Research Agent: Fetches information
  - Coder Agent: Writes code
  - Review Agent: Validates output
"""

AGENT_TOPICS = {
    "tasks": "agent-tasks",
    "planning": "agent-planning",
    "research": "agent-research",
    "coding": "agent-coding",
    "review": "agent-review",
    "results": "agent-results",
}

class AgentOrchestrator:
    def __init__(self):
        self.anthropic = Anthropic()
        self.producer = KafkaProducerService()

    def submit_task(self, task: str, task_id: str = None):
        task_id = task_id or str(uuid.uuid4())
        self.producer.publish(
            topic=AGENT_TOPICS["tasks"],
            key=task_id,
            value={"task_id": task_id, "task": task, "step": "planning"}
        )
        return task_id

class PlannerAgent:
    """Consumes from 'agent-tasks', produces to specialized topics"""

    def run(self):
        consumer = self._create_consumer("planner-agent-group")
        consumer.subscribe([AGENT_TOPICS["tasks"]])
        producer = KafkaProducerService()

        while True:
            messages = consumer.consume(num_messages=1, timeout=1.0)
            for msg in messages:
                task_data = json.loads(msg.value())
                plan = self._plan(task_data['task'])

                # Route subtasks to appropriate agents
                for subtask in plan['subtasks']:
                    if subtask['type'] == 'research':
                        producer.publish(AGENT_TOPICS["research"],
                                         task_data['task_id'], subtask)
                    elif subtask['type'] == 'coding':
                        producer.publish(AGENT_TOPICS["coding"],
                                         task_data['task_id'], subtask)

                consumer.commit(msg)

    def _plan(self, task: str) -> dict:
        response = self.anthropic.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system="""You are a task planner. Break down the given task into subtasks.
            Respond in JSON: {"subtasks": [{"type": "research|coding", "description": "..."}]}""",
            messages=[{"role": "user", "content": task}]
        )
        return json.loads(response.content[0].text)

class ResearchAgent:
    """Consumes from 'agent-research', produces results to 'agent-results'"""

    def run(self):
        consumer = self._create_consumer("research-agent-group")
        consumer.subscribe([AGENT_TOPICS["research"]])
        producer = KafkaProducerService()

        while True:
            messages = consumer.consume(num_messages=1, timeout=1.0)
            for msg in messages:
                subtask = json.loads(msg.value())
                result = self._research(subtask['description'])

                producer.publish(
                    topic=AGENT_TOPICS["results"],
                    key=subtask.get('task_id', 'unknown'),
                    value={
                        "agent": "research",
                        "task_id": subtask.get('task_id'),
                        "result": result,
                        "subtask": subtask
                    }
                )
                consumer.commit(msg)
```

---

## PART 5: Advanced Kafka Patterns

### Exactly-Once Semantics (EOS)

```python
# exactly_once_producer.py
from confluent_kafka import Producer

eos_config = {
    'bootstrap.servers': 'localhost:9092',
    'transactional.id': 'my-unique-producer-id',  # Must be unique per producer
    'enable.idempotence': True,
    'acks': 'all',
}

producer = Producer(eos_config)
producer.init_transactions()

def publish_with_transaction(messages: list):
    producer.begin_transaction()
    try:
        for topic, key, value in messages:
            producer.produce(topic=topic, key=key,
                             value=json.dumps(value))
        producer.commit_transaction()
    except Exception as e:
        producer.abort_transaction()
        raise
```

### Kafka Streams — Real-Time Processing

```python
# Using Faust (Python Kafka Streams equivalent)
import faust

app = faust.App(
    'genai-stream-processor',
    broker='kafka://localhost:9092',
    value_serializer='json',
)

# Define stream topics
llm_requests = app.topic('ai-inference-requests')
llm_responses = app.topic('ai-inference-responses')
metrics_topic = app.topic('ai-metrics')

# Windowed aggregation — count requests per user per minute
user_request_counts = app.Table(
    'user-request-counts',
    default=int,
).tumbling(60.0)  # 60-second tumbling window

@app.agent(llm_requests)
async def process_requests(stream):
    async for request in stream:
        user_id = request['user_id']

        # Update windowed count
        user_request_counts[user_id] += 1
        count = user_request_counts[user_id].current()

        # Rate limiting
        if count > 10:  # 10 requests per minute
            await metrics_topic.send(
                key=user_id,
                value={"event": "rate_limit_exceeded",
                       "user_id": user_id, "count": count}
            )
            continue

        # Forward to LLM worker
        yield request

@app.agent(llm_responses)
async def track_response_times(stream):
    async for response in stream:
        await metrics_topic.send(
            key=response['request_id'],
            value={
                "event": "inference_complete",
                "model": response['model'],
                "tokens": response['usage'].get('output_tokens', 0),
                "status": response['status']
            }
        )
```

### Schema Registry — Data Contracts

```python
# schema_registry.py
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

schema_registry_client = SchemaRegistryClient({
    'url': 'http://schema-registry:8081'
})

# Avro schema for LLM requests
llm_request_schema = """
{
  "type": "record",
  "name": "LLMRequest",
  "fields": [
    {"name": "request_id", "type": "string"},
    {"name": "user_id", "type": "string"},
    {"name": "prompt", "type": "string"},
    {"name": "model", "type": "string", "default": "claude-sonnet-4-6"},
    {"name": "max_tokens", "type": "int", "default": 1000},
    {"name": "timestamp", "type": "long"}
  ]
}
"""

avro_serializer = AvroSerializer(
    schema_registry_client,
    llm_request_schema
)
# Now all messages are validated against schema before publishing
```

---

## PART 6: Production Infrastructure

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ZooKeeper (or use KRaft mode for Kafka 3.x+)
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    volumes:
      - zookeeper_data:/var/lib/zookeeper/data

  kafka-1:
    image: confluentinc/cp-kafka:7.5.0
    depends_on: [zookeeper]
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-1:9092
      KAFKA_NUM_PARTITIONS: 12
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2          # At least 2 replicas must be in sync
      KAFKA_LOG_RETENTION_HOURS: 168        # Keep messages 7 days
      KAFKA_LOG_RETENTION_BYTES: 107374182400  # Max 100GB per partition
      KAFKA_LOG_SEGMENT_BYTES: 1073741824   # 1GB per segment file
      KAFKA_MESSAGE_MAX_BYTES: 10485760     # Max message: 10MB
    volumes:
      - kafka1_data:/var/lib/kafka/data

  kafka-2:
    image: confluentinc/cp-kafka:7.5.0
    depends_on: [zookeeper]
    ports:
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-2:9093
      KAFKA_NUM_PARTITIONS: 12
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2

  kafka-3:
    image: confluentinc/cp-kafka:7.5.0
    depends_on: [zookeeper]
    ports:
      - "9094:9094"
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-3:9094
      KAFKA_NUM_PARTITIONS: 12
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2

  schema-registry:
    image: confluentinc/cp-schema-registry:7.5.0
    depends_on: [kafka-1]
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka-1:9092
      SCHEMA_REGISTRY_HOST_NAME: schema-registry

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: production
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka-1:9092,kafka-2:9093,kafka-3:9094
      KAFKA_CLUSTERS_0_SCHEMAREGISTRY: http://schema-registry:8081

volumes:
  zookeeper_data:
  kafka1_data:
```

### Monitoring & Alerting

```python
# kafka_health_monitor.py
from confluent_kafka.admin import AdminClient, ConfigResource
from prometheus_client import Gauge, Counter, start_http_server
import time

# Prometheus metrics
consumer_lag = Gauge('kafka_consumer_lag',
                     'Consumer group lag',
                     ['topic', 'partition', 'group'])
messages_produced = Counter('kafka_messages_produced_total',
                            'Total messages produced', ['topic'])
broker_count = Gauge('kafka_broker_count', 'Number of active brokers')

class KafkaHealthMonitor:
    def __init__(self, bootstrap_servers: str):
        self.admin = AdminClient({'bootstrap.servers': bootstrap_servers})

    def check_consumer_lag(self, group_id: str, topic: str):
        """Alert if consumer lag exceeds threshold"""
        # For GenAI: lag > 1000 = LLM workers overwhelmed
        ALERT_THRESHOLD = 1000

        metadata = self.admin.list_topics(topic)
        for partition in metadata.topics[topic].partitions.values():
            lag = self._get_partition_lag(group_id, topic, partition.id)
            consumer_lag.labels(
                topic=topic,
                partition=partition.id,
                group=group_id
            ).set(lag)

            if lag > ALERT_THRESHOLD:
                self._send_alert(
                    f"HIGH LAG ALERT: {group_id} lag={lag} "
                    f"on {topic}[{partition.id}]. "
                    f"Scale up LLM workers!"
                )

    def monitor_loop(self):
        start_http_server(9090)  # Prometheus scrape endpoint
        while True:
            self.check_consumer_lag("llm-workers", "ai-inference-requests")
            self.check_consumer_lag("doc-embedders", "document-chunks")
            time.sleep(30)
```

---

## PART 7: GenAI Production Patterns Summary

```
┌─────────────────────────────────────────────────────────────────┐
│               COMPLETE GENAI + KAFKA ARCHITECTURE               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Users/Apps                                                     │
│      │                                                          │
│      ▼                                                          │
│  API Gateway ──► Rate Limiter (Kafka Streams)                   │
│      │                                                          │
│      ├──► [ai-inference-requests] ──► LLM Worker Pool (3-10x)  │
│      │              │                        │                  │
│      │              ▼                        ▼                  │
│      │    Schema Registry            Claude/GPT/Llama           │
│      │                                       │                  │
│      ├──► [document-ingestion]               ▼                  │
│      │         │                    [ai-inference-results]      │
│      │         ▼                             │                  │
│      │    Chunker Workers                    ▼                  │
│      │         │                    WebSocket Server            │
│      │         ▼                    (streams back to user)      │
│      │    [document-chunks]                                     │
│      │         │                                                │
│      │         ▼                                                │
│      │    Embedding Workers                                     │
│      │         │                                                │
│      │         ▼                                                │
│      │    Vector DB (Pinecone/Weaviate)                         │
│      │                                                          │
│      ├──► [agent-tasks] ──► Planner Agent                       │
│      │                          │                               │
│      │              ┌───────────┼───────────┐                   │
│      │              ▼           ▼           ▼                   │
│      │       Research       Coder       Reviewer                │
│      │       Agent          Agent       Agent                   │
│      │              └───────────┼───────────┘                   │
│      │                          ▼                               │
│      │                   [agent-results]                        │
│      │                                                          │
│      └──► [ai-metrics] ──► Monitoring (Prometheus/Grafana)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Production Rules for Kafka + GenAI

| Concern | Rule |
|---|---|
| **Partitioning** | Use `user_id` as key so same user's requests stay ordered |
| **Replication** | Always `replication.factor=3`, `min.insync.replicas=2` |
| **Consumer Groups** | One group per service (llm-workers, embedders, etc.) |
| **Offset Management** | Always manual commit — commit only after successful LLM call |
| **Dead Letter Queue** | Every topic needs a `.dlq` topic for failed messages |
| **Schema Registry** | Enforce Avro/Protobuf schemas to prevent data corruption |
| **Lag Monitoring** | Alert when consumer lag > threshold (LLM workers overwhelmed) |
| **Scaling** | Add more consumer instances = automatic load distribution |
| **Retention** | LLM requests: 24h. Documents: 7 days. Metrics: 30 days |
| **Compression** | Use `snappy` for LLM payloads (fast + good compression) |

---

Kafka is the backbone that makes GenAI systems **scalable, resilient, and observable**. Instead of your API crashing under LLM load, Kafka queues requests, distributes them across worker pools, and streams results back — all with fault tolerance built in.
