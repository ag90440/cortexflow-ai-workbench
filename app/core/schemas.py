from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class IngestRequest(BaseModel):
    source: str
    text: str
    tags: List[str] = Field(default_factory=list)
    owner: str = 'public'
    visibility: str = 'public'

class QueryRequest(BaseModel):
    question: str
    user_id: str = 'demo-user'
    strategy: str = 'hybrid'
    top_k: int = 5
    filters: Dict[str, Any] = Field(default_factory=dict)

class RetrievedChunk(BaseModel):
    chunk_id: str
    source: str
    text: str
    score: float
    rank: int
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RagResponse(BaseModel):
    answer: str
    question: str
    strategy: str
    citations: List[RetrievedChunk]
    metrics: Dict[str, Any]

class ChatRequest(BaseModel):
    message: str
    session_id: str = 'demo-session'
    user_id: str = 'demo-user'
    use_rag: bool = True
    strategy: str = 'hybrid'

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    memory_summary: str
    citations: List[RetrievedChunk] = Field(default_factory=list)
    trace_id: str

class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    requires_approval: bool = False

class AgentRequest(BaseModel):
    goal: str
    session_id: str = 'demo-session'
    user_id: str = 'demo-user'
    approved: bool = False
    pattern: str = 'auto'

class AgentStep(BaseModel):
    step: int
    role: str
    action: str
    input: Dict[str, Any] = Field(default_factory=dict)
    output: Dict[str, Any] = Field(default_factory=dict)
    status: str = 'done'

class AgentResponse(BaseModel):
    goal: str
    pattern: str
    final_answer: str
    steps: List[AgentStep]
    state: Dict[str, Any]
    trace_id: str

class MultiAgentRequest(BaseModel):
    objective: str
    user_id: str = 'demo-user'
    session_id: str = 'multi-agent-demo'

class EvalSample(BaseModel):
    id: str
    question: str
    expected_terms: List[str] = Field(default_factory=list)
    reference_answer: str = ''

class EvalReport(BaseModel):
    name: str
    score: float
    metrics: Dict[str, Any]
    rows: List[Dict[str, Any]]

class JsonRpcRequest(BaseModel):
    jsonrpc: str = '2.0'
    id: str = '1'
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)

class JsonRpcResponse(BaseModel):
    jsonrpc: str = '2.0'
    id: str = '1'
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
