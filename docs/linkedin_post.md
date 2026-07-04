# LinkedIn Post

I built a new GenAI engineering portfolio project: CortexFlow AI Workbench.

Most AI demos stop at a chatbot. I wanted to build something closer to how real AI products are engineered.

CortexFlow brings together the concepts that are becoming important for AI engineers:

- RAG and knowledge Q&A
- Local vector search with BM25, TF-IDF, and hybrid retrieval
- Context engineering
- AI agent workflow with planner, tools, memory, and policy gate
- MCP-style tool, resource, and prompt interface
- Multi-agent workflow with planner, researcher, architect, critic, and finalizer
- LLM evaluation with groundedness, citation coverage, safety, token F1, and latency
- RL-style retrieval strategy tuning using a bandit
- Computer-use action planning with approval gates
- AI coding workflow helper
- ML system design blueprint generator
- Fine-tuning dataset export from traces
- FastAPI backend, Streamlit UI, Docker, tests, and documentation

The main idea behind the project:

AI engineering is not only about calling an LLM. It is about building a reliable system around the model.

A production AI app needs retrieval, permissions, tool schemas, memory, state, evaluation, observability, and safe fallback behavior.

I kept the project local-first so anyone can run it without paid API keys. It also supports optional Ollama and OpenAI-compatible providers.

This project helped me understand GenAI from a system-design point of view:

- When to use RAG vs agent workflows
- Why tool execution must be controlled by backend policy
- Why evals are needed before shipping
- Why memory and state are hard
- Why multi-agent systems should be used only when the task truly needs specialization

Tech stack:
Python, FastAPI, Streamlit, Pydantic, local retrieval, MCP-style JSON-RPC, EvalOps, Docker, Pytest.

I am continuing to build deeper in GenAI engineering, agentic systems, MCP, RAG evaluation, and AI product infrastructure.

GitHub repo coming soon.

#GenAI #AIAgents #RAG #MCP #LLM #FastAPI #Python #AIEngineering #MachineLearning #SystemDesign #OpenSource
