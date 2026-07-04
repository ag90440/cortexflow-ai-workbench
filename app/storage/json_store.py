from pathlib import Path
from typing import Any
import json
import time
import uuid

class JsonStore:
    def __init__(self, path: Path, default: Any):
        self.path = Path(path)
        self.default = default
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write(default)

    def read(self) -> Any:
        try:
            return json.loads(self.path.read_text(encoding='utf-8'))
        except Exception:
            return self.default

    def write(self, data: Any) -> None:
        tmp = self.path.with_suffix(self.path.suffix + '.tmp')
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        tmp.replace(self.path)

    def append(self, item: Any) -> Any:
        data = self.read()
        if not isinstance(data, list):
            data = []
        data.append(item)
        self.write(data)
        return item

    def event(self, kind: str, payload: Any) -> dict:
        return {
            'id': str(uuid.uuid4()),
            'kind': kind,
            'payload': payload,
            'created_at': time.time()
        }
