# Topic Coverage Matrix

This project was designed around the AI engineer concept list from the uploaded learning pack. Each concept is mapped to a working module, endpoint, and demo story.

| AI engineer topic | Where it exists in CortexFlow | How to demo it |
|---|---|---|
| LLM evals | `app/evals` and `/eval/run` | Run EvalOps and show groundedness, citation coverage, safety, token F1 |
| Knowledge Q&A system | `app/rag/pipeline.py` | Ask a question from sample docs and show cited chunks |
| OpenClaw/computer-use architecture | `app/agents/computer_use.py` | Ask for a browser task and show observe, navigate, type, verify, approval steps |
| AI agent workflow | `app/agents/runner.py` | Run `/agent/run` and show planner, policy, executor, reflection |
| MCP | `app/mcp/server.py` | Call `tools/list`, `tools/call`, `resources/list`, and `prompts/list` |
| AI chat assistant | `/chat` and `ui/streamlit_app.py` | Show memory summary and optional RAG citations |
| RAG | `app/rag` | Ingest, retrieve, generate answer, return citations |
| Agentic patterns | `app/agents/patterns.py` | Show router, ReAct-style tool loop, planner-executor, evaluator-optimizer |
| AI coding workflow | `app/coding/workflow.py` | Submit a feature request and show plan, test ideas, review loop |
| ML system design | `app/system_design/blueprints.py` | Generate an AI system blueprint from a requirement |
| Multi-agent architecture | `app/agents/multi_agent.py` | Run planner, researcher, architect, critic, finalizer |
| How AI agents work | Agent runtime plus tool registry | Explain model, tools, state, memory, policy, evals |
| Vector database | `app/rag/vector_store.py` | Show BM25, TF-IDF, keyword, hybrid strategies |
| Memory and state | `app/memory/store.py` | Show session events, long-term facts, versioning |
| AI agent design | `PolicyGate`, `PatternSelector`, `ToolRegistry` | Explain autonomy level, risk, tool access, approval |
| Context engineering | `app/context/engine.py` | Show how goal, evidence, memory, and tool traces form context |
| Reinforcement learning | `app/rl/bandit.py` | Update reward for retrieval strategy and show leaderboard |
| LLM concepts | `app/llm/providers.py` and docs | Explain tokens, context, model routing, local vs hosted providers |
| Fine-tuning | `app/training/dataset_builder.py` | Export SFT JSONL and preference pairs from traces |
| Local LLMs | `ModelRouter` with Ollama mode | Set provider to Ollama and run same endpoints |
| LangChain/LangGraph style thinking | Planner, graph-like steps, stateful workflow | Explain how this can be swapped with LangChain tools or LangGraph nodes |

## How to explain the project simply

CortexFlow is a mini AI platform. It starts with a question, retrieves private knowledge, builds context, lets an agent call safe tools, stores memory, evaluates the result, and exports useful traces for future improvement.

## How to explain the project technically

The app is a modular AI control plane. The RAG layer handles evidence, the agent layer handles decisions and tool calls, the MCP layer exposes capabilities, the EvalOps layer measures quality, and the training layer converts traces into datasets. The design is local-first but production-inspired.
