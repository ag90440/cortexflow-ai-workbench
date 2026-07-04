from pathlib import Path
from typing import Dict, List
from app.core.config import settings
from app.core.schemas import EvalReport
from app.evals.metrics import citation_coverage, expected_term_recall, groundedness, safety_score, token_f1
from app.rag.pipeline import RagPipeline
import json
import time

class EvalRunner:
    def __init__(self, rag: RagPipeline | None = None):
        self.rag = rag or RagPipeline()

    def run_file(self, name: str = 'rag_eval.json') -> EvalReport:
        path = settings.eval_sets_dir / name
        samples = json.loads(path.read_text(encoding='utf-8'))
        rows = []
        started = time.time()
        for sample in samples:
            response = self.rag.answer(sample['question'], strategy=sample.get('strategy', 'hybrid'), top_k=sample.get('top_k', 5))
            contexts = [item.text for item in response.citations]
            citation_ids = [item.chunk_id for item in response.citations]
            row = {
                'id': sample['id'],
                'question': sample['question'],
                'answer': response.answer,
                'term_recall': expected_term_recall(response.answer, sample.get('expected_terms', [])),
                'token_f1': token_f1(response.answer, sample.get('reference_answer', '')),
                'groundedness': groundedness(response.answer, contexts),
                'citation_coverage': citation_coverage(response.answer, citation_ids),
                'safety': safety_score(response.answer),
                'latency_ms': response.metrics['latency_ms']
            }
            rows.append(row)
        metrics = self._aggregate(rows)
        metrics['total_latency_ms'] = round((time.time() - started) * 1000, 2)
        return EvalReport(name=name, score=metrics['overall'], metrics=metrics, rows=rows)

    def _aggregate(self, rows: List[Dict]) -> Dict:
        if not rows:
            return {'overall': 0.0}
        keys = ['term_recall', 'token_f1', 'groundedness', 'citation_coverage', 'safety']
        metrics = {key: round(sum(row[key] for row in rows) / len(rows), 4) for key in keys}
        metrics['overall'] = round(sum(metrics[key] for key in keys) / len(keys), 4)
        metrics['samples'] = len(rows)
        return metrics
