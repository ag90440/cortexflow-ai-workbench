from typing import Dict, List
from app.core.config import settings

class ContextEngine:
    def build(self, user_goal: str, retrieved: List[Dict], memory: List[Dict], tool_trace: List[Dict] | None = None) -> List[Dict[str, str]]:
        tool_trace = tool_trace or []
        system = 'You are CortexFlow, a reliable AI workbench. Use evidence first, call tools only through approved schemas, and explain uncertainty.'
        memory_text = self._trim('\n'.join(item.get('text', '') for item in memory), settings.max_context_words // 4)
        retrieval_text = self._trim('\n\n'.join(f"[{item.get('chunk_id')}] {item.get('text')}" for item in retrieved), settings.max_context_words // 2)
        trace_text = self._trim('\n'.join(str(item) for item in tool_trace), settings.max_context_words // 4)
        user = f'Goal: {user_goal}\n\nRelevant memory:\n{memory_text}\n\nRetrieved evidence:\n{retrieval_text}\n\nTool trace:\n{trace_text}'
        return [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]

    def _trim(self, text: str, max_words: int) -> str:
        words = text.split()
        if len(words) <= max_words:
            return text
        return ' '.join(words[:max_words])
