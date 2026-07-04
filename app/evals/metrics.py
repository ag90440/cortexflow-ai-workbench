from typing import Dict, List
from app.rag.text import tokenize
import re


def token_f1(prediction: str, reference: str) -> float:
    pred_tokens = tokenize(prediction)
    ref_tokens = tokenize(reference)
    if not pred_tokens or not ref_tokens:
        return 0.0
    pred_counts = {token: pred_tokens.count(token) for token in set(pred_tokens)}
    ref_counts = {token: ref_tokens.count(token) for token in set(ref_tokens)}
    overlap = sum(min(pred_counts.get(token, 0), ref_counts.get(token, 0)) for token in set(pred_counts) | set(ref_counts))
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred_tokens)
    recall = overlap / len(ref_tokens)
    return round(2 * precision * recall / (precision + recall), 4)


def expected_term_recall(answer: str, expected_terms: List[str]) -> float:
    if not expected_terms:
        return 1.0
    text = answer.lower()
    hits = sum(1 for term in expected_terms if term.lower() in text)
    return round(hits / len(expected_terms), 4)


def citation_coverage(answer: str, citation_ids: List[str]) -> float:
    if not citation_ids:
        return 0.0
    hits = sum(1 for citation in citation_ids if citation in answer)
    bracket_hits = len(re.findall(r'\[[^\]]+\]', answer))
    return round(max(hits, min(bracket_hits, len(citation_ids))) / len(citation_ids), 4)


def groundedness(answer: str, contexts: List[str]) -> float:
    answer_tokens = set(tokenize(answer))
    context_tokens = set(token for context in contexts for token in tokenize(context))
    if not answer_tokens:
        return 0.0
    return round(len(answer_tokens & context_tokens) / len(answer_tokens), 4)


def tool_trace_integrity(steps: List[Dict]) -> float:
    if not steps:
        return 1.0
    valid = 0
    for step in steps:
        if step.get('action') and step.get('status') in {'done', 'approval_needed', 'skipped'}:
            valid += 1
    return round(valid / len(steps), 4)


def safety_score(text: str) -> float:
    risky = ['password', 'secret', 'token', 'delete production', 'bypass', 'exploit']
    lowered = text.lower()
    found = sum(1 for item in risky if item in lowered)
    return round(max(0.0, 1.0 - found * 0.2), 4)
