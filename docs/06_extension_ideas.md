# Extension Ideas

## Production upgrades

- Replace local JSON stores with PostgreSQL.
- Replace local sparse index with pgvector, Qdrant, Weaviate, Milvus, or Elasticsearch.
- Add authentication and RBAC.
- Add per-document permission filtering before retrieval.
- Add streaming responses.
- Add background ingestion jobs.
- Add document parsing for PDF, DOCX, HTML, CSV, and images.
- Add reranker model.
- Add distributed tracing.
- Add prompt registry and prompt versioning.
- Add model cost tracking.
- Add CI-based evaluation gate.

## Agent upgrades

- Add dynamic planning with actual LLM tool selection.
- Add human approval UI.
- Add idempotency keys for write tools.
- Add tool retry policy.
- Add tool timeouts.
- Add tool-level auth scopes.
- Add execution sandbox for computer-use workflows.

## Eval upgrades

- Add human annotation UI.
- Add pairwise model comparison.
- Add RAGAS-style metrics.
- Add prompt regression tests.
- Add dataset versioning.
- Add slice-based eval reports by topic, source, and user role.

## Fine-tuning upgrades

- Add trace filtering.
- Add privacy redaction.
- Add dataset quality scoring.
- Add LoRA training notebook.
- Add DPO preference dataset generation.
- Add model comparison after fine-tuning.
