from collections import Counter, defaultdict
from typing import Dict, List
from app.rag.text import tokenize, term_counts, cosine
import math

class LocalVectorIndex:
    def __init__(self, chunks: List[Dict] | None = None):
        self.chunks = chunks or []
        self.doc_terms: List[Counter] = []
        self.idf: Dict[str, float] = {}
        self.avg_len = 1.0
        if self.chunks:
            self.build(self.chunks)

    def build(self, chunks: List[Dict]) -> None:
        self.chunks = chunks
        self.doc_terms = [term_counts(item.get('text', '')) for item in chunks]
        doc_frequency = defaultdict(int)
        for terms in self.doc_terms:
            for token in terms:
                doc_frequency[token] += 1
        total = max(1, len(chunks))
        self.idf = {token: math.log(1 + (total - count + 0.5) / (count + 0.5)) for token, count in doc_frequency.items()}
        lengths = [sum(terms.values()) for terms in self.doc_terms]
        self.avg_len = sum(lengths) / max(1, len(lengths))

    def query(self, query: str, top_k: int = 5, strategy: str = 'hybrid', filters: Dict | None = None) -> List[Dict]:
        filters = filters or {}
        query_terms = term_counts(query)
        rows = []
        for position, chunk in enumerate(self.chunks):
            if not self._allowed(chunk, filters):
                continue
            terms = self.doc_terms[position]
            bm25 = self._bm25(query_terms, terms)
            sparse = cosine(query_terms, terms)
            keyword = self._keyword_overlap(query_terms, terms)
            if strategy == 'bm25':
                score = bm25
            elif strategy == 'tfidf':
                score = sparse
            elif strategy == 'keyword':
                score = keyword
            else:
                score = 0.55 * bm25 + 0.30 * sparse + 0.15 * keyword
            if score > 0:
                rows.append({**chunk, 'score': round(float(score), 6)})
        rows.sort(key=lambda item: item['score'], reverse=True)
        return [{**row, 'rank': index + 1} for index, row in enumerate(rows[:top_k])]

    def _allowed(self, chunk: Dict, filters: Dict) -> bool:
        metadata = chunk.get('metadata', {})
        for key, value in filters.items():
            if value is None or value == '':
                continue
            if metadata.get(key) != value:
                return False
        return True

    def _bm25(self, query_terms: Counter, doc_terms: Counter) -> float:
        k1 = 1.5
        b = 0.75
        doc_len = sum(doc_terms.values()) or 1
        score = 0.0
        for token, q_count in query_terms.items():
            frequency = doc_terms.get(token, 0)
            if frequency == 0:
                continue
            idf = self.idf.get(token, 0.0)
            numerator = frequency * (k1 + 1)
            denominator = frequency + k1 * (1 - b + b * doc_len / max(self.avg_len, 1))
            score += idf * numerator / max(denominator, 1e-9) * q_count
        return score

    def _keyword_overlap(self, query_terms: Counter, doc_terms: Counter) -> float:
        query_keys = set(query_terms)
        doc_keys = set(doc_terms)
        if not query_keys:
            return 0.0
        return len(query_keys & doc_keys) / len(query_keys)
