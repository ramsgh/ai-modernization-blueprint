# Low-Level Design

## Component Design

### CDC Connector

- Captures row-level changes from source ERP tables.
- Publishes normalized event envelopes to Kafka.
- Uses schema registry for compatibility checks.
- Supports replay from source offsets where available.

### Kafka Topic Strategy

Topic naming convention:

```text
<domain>.<entity>.<event-type>.v<major-version>
```

Example:

```text
erp.purchase_order.changed.v1
```

Topic standards:

- Use Avro or Protobuf schemas for enterprise data contracts.
- Enable compaction for reference data topics.
- Use retention policies aligned to replay and compliance requirements.
- Use dead-letter topics for poison messages and validation failures.

### Flink Processing

Flink jobs perform:

- Event validation
- PII redaction or tokenization
- Reference-data enrichment
- Windowed aggregations
- Lakehouse writes
- Embedding trigger events

### Lakehouse Data Zones

| Zone | Purpose |
| --- | --- |
| Bronze | Raw append-only ingestion |
| Silver | Cleaned and conformed events |
| Gold | Business-owned data products |

### Vector Indexing

Embedding pipelines should:

- Chunk documents and long records deterministically.
- Attach source lineage, ownership, access labels, and refresh timestamps.
- Separate indexes by domain and access class where required.
- Support deletion and re-indexing for retention and privacy obligations.

### LLM Gateway

Gateway responsibilities:

- Model routing
- Prompt template management
- Policy enforcement
- Retrieval orchestration
- Token and cost tracking
- Response logging
- Human feedback capture

## Security Controls

- Workload identity for services.
- Private networking for data stores.
- Encryption in transit and at rest.
- Centralized secret storage.
- Role-based and attribute-based access controls.
- Audit logging for prompt, retrieval, and model invocation metadata.

## Operational Runbooks

### Pipeline Failure

1. Check Flink job health and checkpoint status.
2. Inspect Kafka consumer lag.
3. Review dead-letter topic records.
4. Validate schema registry compatibility.
5. Replay from the last known good offset after remediation.

### Retrieval Quality Issue

1. Confirm source data freshness.
2. Inspect chunking and embedding metadata.
3. Review retrieval trace and top-k results.
4. Validate access filters.
5. Capture user feedback and update evaluation datasets.

## Environment Promotion

Recommended environments:

- `dev`: fast iteration and synthetic test data
- `test`: integration testing with masked data
- `stage`: production-like performance and security validation
- `prod`: controlled release with full audit evidence
