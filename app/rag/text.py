from collections import Counter
from typing import List
import math
import re

STOPWORDS = {'the', 'a', 'an', 'of', 'to', 'in', 'and', 'or', 'for', 'with', 'on', 'is', 'are', 'as', 'by', 'from', 'that', 'this', 'it'}


def tokenize(text: str) -> List[str]:
    tokens = re.findall(r'[a-zA-Z0-9_]+', text.lower())
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def term_counts(text: str) -> Counter:
    return Counter(tokenize(text))


def cosine(left: Counter, right: Counter) -> float:
    keys = set(left) | set(right)
    if not keys:
        return 0.0
    numerator = sum(left.get(k, 0) * right.get(k, 0) for k in keys)
    left_norm = math.sqrt(sum(v * v for v in left.values()))
    right_norm = math.sqrt(sum(v * v for v in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def split_words(text: str) -> List[str]:
    return re.findall(r'\S+', text)
