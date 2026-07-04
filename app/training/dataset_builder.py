from app.core.config import settings
from app.storage.json_store import JsonStore
from pathlib import Path
from typing import Dict, List
import json

class FineTuningDatasetBuilder:
    def __init__(self):
        self.rag_traces = JsonStore(settings.runtime_dir / 'rag_traces.json', [])

    def build_sft_records(self) -> List[Dict]:
        records = []
        for trace in self.rag_traces.read():
            question = trace.get('question', '')
            answer = trace.get('answer', '')
            if question and answer:
                records.append({'messages': [{'role': 'system', 'content': 'Answer using enterprise context and cite uncertainty.'}, {'role': 'user', 'content': question}, {'role': 'assistant', 'content': answer}]})
        return records

    def build_preference_records(self) -> List[Dict]:
        records = []
        for trace in self.rag_traces.read():
            question = trace.get('question', '')
            answer = trace.get('answer', '')
            if question and answer:
                rejected = 'I do not know, but here is a confident answer without evidence.'
                records.append({'prompt': question, 'chosen': answer, 'rejected': rejected})
        return records

    def export_jsonl(self, path: str, mode: str = 'sft') -> Dict:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        records = self.build_sft_records() if mode == 'sft' else self.build_preference_records()
        output.write_text('\n'.join(json.dumps(record, ensure_ascii=False) for record in records), encoding='utf-8')
        return {'path': str(output), 'records': len(records), 'mode': mode}
