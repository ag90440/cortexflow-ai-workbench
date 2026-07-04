from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Settings:
    app_name: str = 'CortexFlow AI Workbench'
    version: str = '1.0.0'
    project_root: Path = Path(__file__).resolve().parents[2]
    runtime_dir: Path = Path(os.getenv('CORTEXFLOW_RUNTIME_DIR', Path(__file__).resolve().parents[2] / 'data' / 'runtime'))
    sample_docs_dir: Path = Path(os.getenv('CORTEXFLOW_SAMPLE_DOCS_DIR', Path(__file__).resolve().parents[2] / 'data' / 'sample_docs'))
    eval_sets_dir: Path = Path(os.getenv('CORTEXFLOW_EVAL_SETS_DIR', Path(__file__).resolve().parents[2] / 'data' / 'eval_sets'))
    model_provider: str = os.getenv('CORTEXFLOW_MODEL_PROVIDER', 'local')
    ollama_url: str = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
    ollama_model: str = os.getenv('OLLAMA_MODEL', 'llama3.1')
    openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
    openai_model: str = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    max_context_words: int = int(os.getenv('CORTEXFLOW_MAX_CONTEXT_WORDS', '1200'))
    default_top_k: int = int(os.getenv('CORTEXFLOW_TOP_K', '5'))

settings = Settings()
settings.runtime_dir.mkdir(parents=True, exist_ok=True)
