from pathlib import Path
from typing import Dict, List
from app.core.config import settings
from app.core.schemas import RagResponse, RetrievedChunk
from app.llm.providers import ModelRouter
from app.rag.chunker import chunk_text
from app.rag.vector_store import LocalVectorIndex
from app.storage.json_store import JsonStore
import time

class RagPipeline:
    def __init__(self):
        self.chunk_store = JsonStore(settings.runtime_dir / 'chunks.json', [])
        self.trace_store = JsonStore(settings.runtime_dir / 'rag_traces.json', [])
        self.model = ModelRouter()
        self.index = LocalVectorIndex(self._load_chunks())
        if not self.index.chunks:
            self.ingest_sample_documents()

    def _load_chunks(self) -> List[Dict]:
        return self.chunk_store.read()

    def _save_chunks(self, chunks: List[Dict]) -> None:
        self.chunk_store.write(chunks)
        self.index.build(chunks)

    def ingest_sample_documents(self) -> int:
        added = 0
        for path in sorted(settings.sample_docs_dir.glob('*.md')):
            text = path.read_text(encoding='utf-8')
            added += self.ingest_text(path.name, text, tags=['sample'], owner='public', visibility='public')
        return added

    def ingest_text(self, source: str, text: str, tags: List[str] | None = None, owner: str = 'public', visibility: str = 'public') -> int:
        metadata = {'tags': tags or [], 'owner': owner, 'visibility': visibility, 'created_at': time.time()}
        new_chunks = chunk_text(source, text, metadata)
        chunks = [item for item in self._load_chunks() if item.get('source') != source]
        chunks.extend(new_chunks)
        self._save_chunks(chunks)
        return len(new_chunks)

    def retrieve(self, question: str, user_id: str = 'demo-user', strategy: str = 'hybrid', top_k: int = 5, filters: Dict | None = None) -> List[Dict]:
        filters = filters or {}
        rows = self.index.query(question, top_k=top_k, strategy=strategy, filters=filters)
        allowed = []
        for row in rows:
            visibility = row.get('metadata', {}).get('visibility', 'public')
            owner = row.get('metadata', {}).get('owner', 'public')
            if visibility == 'public' or owner == user_id:
                allowed.append(row)
        return allowed

    def answer(self, question: str, user_id: str = 'demo-user', strategy: str = 'hybrid', top_k: int = 5, filters: Dict | None = None) -> RagResponse:
        started = time.time()
        rows = self.retrieve(question, user_id=user_id, strategy=strategy, top_k=top_k, filters=filters)
        context = self._format_context(rows)
        answer = self.model.generate([
            {'role': 'system', 'content': 'You answer with only retrieved evidence. Cite chunk ids when possible. Say what is unknown.'},
            {'role': 'user', 'content': f'Question: {question}\n\nContext:\n{context}'}
        ])
        citations = [RetrievedChunk(**row) for row in rows]
        metrics = {
            'retrieved': len(rows),
            'latency_ms': round((time.time() - started) * 1000, 2),
            'strategy': strategy,
            'sources': sorted({row.get('source', '') for row in rows})
        }
        self.trace_store.append({'question': question, 'answer': answer, 'metrics': metrics, 'citations': [row['chunk_id'] for row in rows], 'created_at': time.time()})
        return RagResponse(answer=answer, question=question, strategy=strategy, citations=citations, metrics=metrics)

    def _format_context(self, rows: List[Dict]) -> str:
        blocks = []
        for row in rows:
            blocks.append(f"[{row['chunk_id']}] {row['text']}")
        return '\n\n'.join(blocks)
