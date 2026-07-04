from app.agents.runner import AgentRunner
from app.agents.tools import ToolRegistry
from app.evals.runner import EvalRunner
from app.mcp.server import LocalMcpServer
from app.memory.store import MemoryStore
from app.rag.pipeline import RagPipeline

rag = RagPipeline()
memory = MemoryStore()
registry = ToolRegistry(rag, memory)
agent_runner = AgentRunner(registry, memory)
eval_runner = EvalRunner(rag)
mcp_server = LocalMcpServer(registry, rag)
