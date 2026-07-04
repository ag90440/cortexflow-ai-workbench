from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.agents.multi_agent import MultiAgentCoordinator
from app.core.schemas import AgentRequest, MultiAgentRequest
from app.dependencies import agent_runner, eval_runner, rag
import json

question = 'How should an enterprise AI agent use tools safely?'
print(json.dumps(rag.answer(question).model_dump(), indent=2))
print(json.dumps(agent_runner.run(AgentRequest(goal='Design a safe RAG agent with MCP tools and evaluation')).model_dump(), indent=2))
print(json.dumps(MultiAgentCoordinator(rag).run(MultiAgentRequest(objective='Design an EvalOps dashboard for RAG')).copy(), indent=2))
print(json.dumps(eval_runner.run_file().model_dump(), indent=2))
