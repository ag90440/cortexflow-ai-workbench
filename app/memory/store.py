from app.core.config import settings
from app.storage.json_store import JsonStore
from app.rag.text import tokenize
from typing import Dict, List
import time
import uuid

class MemoryStore:
    def __init__(self):
        self.store = JsonStore(settings.runtime_dir / 'memory.json', {'sessions': {}, 'long_term': []})

    def add_event(self, session_id: str, role: str, text: str, metadata: Dict | None = None) -> Dict:
        data = self.store.read()
        sessions = data.setdefault('sessions', {})
        session = sessions.setdefault(session_id, {'version': 0, 'events': []})
        session['version'] += 1
        event = {'id': str(uuid.uuid4()), 'role': role, 'text': text, 'metadata': metadata or {}, 'created_at': time.time(), 'version': session['version']}
        session['events'].append(event)
        self.store.write(data)
        return event

    def read_session(self, session_id: str, limit: int = 10) -> List[Dict]:
        data = self.store.read()
        events = data.get('sessions', {}).get(session_id, {}).get('events', [])
        return events[-limit:]

    def summarize_session(self, session_id: str) -> str:
        events = self.read_session(session_id, limit=8)
        if not events:
            return 'No memory yet.'
        return ' | '.join(f"{event.get('role')}: {event.get('text')[:100]}" for event in events)

    def remember_fact(self, user_id: str, text: str, tags: List[str] | None = None) -> Dict:
        data = self.store.read()
        fact = {'id': str(uuid.uuid4()), 'user_id': user_id, 'text': text, 'tags': tags or [], 'created_at': time.time()}
        data.setdefault('long_term', []).append(fact)
        self.store.write(data)
        return fact

    def search(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        data = self.store.read()
        query_tokens = set(tokenize(query))
        rows = []
        for fact in data.get('long_term', []):
            if fact.get('user_id') not in {user_id, 'public'}:
                continue
            tokens = set(tokenize(fact.get('text', '')))
            score = len(query_tokens & tokens)
            if score > 0:
                rows.append({**fact, 'score': score})
        rows.sort(key=lambda item: item['score'], reverse=True)
        return rows[:limit]
