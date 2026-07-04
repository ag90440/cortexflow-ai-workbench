from fastapi import APIRouter
from app.agents.multi_agent import MultiAgentCoordinator
from app.core.config import settings
from app.core.schemas import AgentRequest, ChatRequest, ChatResponse, IngestRequest, JsonRpcRequest, MultiAgentRequest, QueryRequest
from app.dependencies import agent_runner, eval_runner, mcp_server, memory, rag, registry
from app.llm.providers import ModelRouter
from app.rl.bandit import RetrievalBandit
from app.training.dataset_builder import FineTuningDatasetBuilder
from app.coding.workflow import CodingWorkflow
from app.system_design.blueprints import SystemDesignBlueprint
import time
import uuid

router = APIRouter()

@router.get('/health')
def health():
    return {'ok': True, 'app': settings.app_name, 'version': settings.version}

@router.post('/ingest')
def ingest(request: IngestRequest):
    count = rag.ingest_text(request.source, request.text, request.tags, request.owner, request.visibility)
    return {'source': request.source, 'chunks': count}

@router.post('/rag/query')
def query(request: QueryRequest):
    return rag.answer(request.question, request.user_id, request.strategy, request.top_k, request.filters)

@router.post('/chat')
def chat(request: ChatRequest):
    trace_id = str(uuid.uuid4())
    memory.add_event(request.session_id, 'user', request.message, {'trace_id': trace_id})
    citations = []
    context = ''
    if request.use_rag:
        rag_response = rag.answer(request.message, request.user_id, request.strategy)
        citations = rag_response.citations
        context = rag_response.answer
    messages = [{'role': 'system', 'content': 'Be useful, concise, grounded, and clear.'}, {'role': 'user', 'content': f'{request.message}\n\nRetrieved answer:\n{context}\n\nMemory:\n{memory.summarize_session(request.session_id)}'}]
    answer = ModelRouter().generate(messages)
    memory.add_event(request.session_id, 'assistant', answer, {'trace_id': trace_id})
    return ChatResponse(answer=answer, session_id=request.session_id, memory_summary=memory.summarize_session(request.session_id), citations=citations, trace_id=trace_id)

@router.post('/agent/run')
def run_agent(request: AgentRequest):
    return agent_runner.run(request)

@router.post('/multiagent/run')
def run_multi_agent(request: MultiAgentRequest):
    return MultiAgentCoordinator(rag).run(request)

@router.post('/mcp')
def mcp(request: JsonRpcRequest):
    return mcp_server.handle(request)

@router.get('/tools')
def tools():
    return {'tools': registry.list_tools()}

@router.post('/eval/run')
def run_eval(name: str = 'rag_eval.json'):
    return eval_runner.run_file(name)

@router.get('/rl/strategy')
def choose_strategy(epsilon: float = 0.1):
    bandit = RetrievalBandit()
    return {'strategy': bandit.choose(epsilon), 'leaderboard': bandit.leaderboard()}

@router.post('/rl/reward')
def update_reward(arm: str, reward: float):
    bandit = RetrievalBandit()
    return bandit.update(arm, reward)

@router.post('/coding/plan')
def coding_plan(request: dict):
    return CodingWorkflow().build_plan(request.get('request', ''))

@router.post('/system-design/blueprint')
def system_design(request: dict):
    return SystemDesignBlueprint().build(request.get('requirement', ''))

@router.post('/training/export')
def export_training(path: str = 'data/runtime/sft.jsonl', mode: str = 'sft'):
    return FineTuningDatasetBuilder().export_jsonl(path, mode)
