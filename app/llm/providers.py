from typing import Dict, List
from app.core.config import settings
import json
import os
import re

try:
    import httpx
except Exception:
    httpx = None

class LocalModel:
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        joined = '\n'.join(m.get('content', '') for m in messages)
        question = self._last_user(messages)
        facts = self._facts(joined)
        if not facts:
            facts = ['Use retrieved evidence, tool results, and memory before answering.', 'Prefer a safe workflow over uncontrolled autonomy.', 'Return a direct answer with practical next steps.']
        body = []
        body.append(f'Answer for: {question}')
        body.append('Key points:')
        for item in facts[:5]:
            body.append(f'- {item}')
        body.append('Suggested next step: validate the answer with evals, traces, and user feedback before shipping.')
        return '\n'.join(body)

    def _last_user(self, messages: List[Dict[str, str]]) -> str:
        for message in reversed(messages):
            if message.get('role') == 'user':
                return message.get('content', '').strip()
        return 'the request'

    def _facts(self, text: str) -> List[str]:
        lines = []
        for raw in re.split(r'[\n\.;]', text):
            item = raw.strip()
            if len(item) > 28 and item.lower() not in {'context', 'answer'}:
                lines.append(item[:220])
        clean = []
        seen = set()
        for item in lines:
            key = item.lower()
            if key not in seen:
                clean.append(item)
                seen.add(key)
        return clean

class OllamaModel:
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        if httpx is None:
            return LocalModel().generate(messages, temperature)
        prompt = '\n'.join(f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages)
        payload = {'model': settings.ollama_model, 'prompt': prompt, 'stream': False, 'options': {'temperature': temperature}}
        try:
            response = httpx.post(settings.ollama_url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get('response', '').strip()
        except Exception:
            return LocalModel().generate(messages, temperature)

class OpenAIModel:
    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        if httpx is None or not settings.openai_api_key:
            return LocalModel().generate(messages, temperature)
        payload = {'model': settings.openai_model, 'messages': messages, 'temperature': temperature}
        headers = {'Authorization': f'Bearer {settings.openai_api_key}', 'Content-Type': 'application/json'}
        try:
            response = httpx.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        except Exception:
            return LocalModel().generate(messages, temperature)

class ModelRouter:
    def __init__(self, provider: str = ''):
        self.provider = provider or settings.model_provider

    def client(self):
        if self.provider == 'ollama':
            return OllamaModel()
        if self.provider == 'openai':
            return OpenAIModel()
        return LocalModel()

    def generate(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        return self.client().generate(messages, temperature)
