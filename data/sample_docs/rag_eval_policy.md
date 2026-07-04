# RAG and Evaluation Policy

A reliable RAG system starts with clean ingestion. Documents should be parsed, chunked, tagged with metadata, protected with permissions, indexed with lexical and semantic retrieval, reranked, and assembled into a concise context window.

Evaluation should measure retrieval quality and answer quality separately. Retrieval metrics include precision at k, recall at k, mean reciprocal rank, and context relevance. Answer metrics include groundedness, citation coverage, answer correctness, safety, latency, and cost per query.

A RAG answer should cite evidence. If evidence is missing, the assistant should say what is unknown rather than inventing an answer.
