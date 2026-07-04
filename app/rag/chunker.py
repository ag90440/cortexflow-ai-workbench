from typing import Dict, List
from app.rag.text import split_words
import hashlib


def chunk_text(source: str, text: str, metadata: Dict, max_words: int = 150, overlap: int = 30) -> List[Dict]:
    words = split_words(text)
    chunks = []
    start = 0
    index = 0
    while start < len(words):
        end = min(len(words), start + max_words)
        chunk_words = words[start:end]
        chunk_text_value = ' '.join(chunk_words).strip()
        if chunk_text_value:
            digest = hashlib.sha1(f'{source}:{index}:{chunk_text_value[:80]}'.encode('utf-8')).hexdigest()[:12]
            chunks.append({
                'chunk_id': f'{source}-{digest}',
                'source': source,
                'text': chunk_text_value,
                'metadata': {**metadata, 'chunk_index': index, 'word_count': len(chunk_words)}
            })
        if end == len(words):
            break
        start = max(0, end - overlap)
        index += 1
    return chunks
