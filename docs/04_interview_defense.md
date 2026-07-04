# Interview Defense Notes

Use this file to explain CortexFlow in interviews.

## Tell me about this project

CortexFlow is a local-first AI engineering workbench that combines RAG, agents, MCP-style tool use, memory, multi-agent workflows, LLM evaluation, RL-style feedback, and fine-tuning dataset export. I built it to show production-style thinking around LLM apps rather than only a chatbot wrapper.

## Why did you build it this way?

I wanted each AI engineering concept to map to real code. RAG has its own pipeline. Tools have a registry. Agents have a planner and policy gate. Memory has versioned state. Evaluation has metrics. MCP has JSON-RPC methods. This makes the project easier to debug and defend.

## Why local-first?

A portfolio project should run without paid keys. The default local model is deterministic so tests can run. The model router also supports Ollama and OpenAI-compatible usage when keys or local models are available.

## Why not just use LangChain or LangGraph everywhere?

For learning and interviews, I wanted the core mechanics to be visible. The architecture can later be swapped to LangChain tools or LangGraph nodes. Building a simple version by hand makes it easier to explain what the frameworks do internally.

## What is the hardest part?

The hardest part is not calling an LLM. It is making the system reliable. You need safe tool execution, permission checks, retrieval quality, context control, memory consistency, evaluation datasets, and observability.

## How would you improve it for production?

I would add real authentication, database persistence, background jobs, distributed tracing, a real vector database, document parsers, reranking models, streaming responses, prompt/version registry, human feedback UI, policy-as-code, secrets manager, and CI-based eval gates.

## How do you calculate impact?

For a real deployment, I would measure:

- Answer correctness
- Retrieval precision and recall
- Groundedness
- Citation correctness
- Tool success rate
- Escalation reduction
- Time saved per task
- p95 latency
- Cost per successful task
- Human override rate

## How does this show GenAI engineer readiness?

It proves I can connect application engineering with AI concepts. The project has backend APIs, UI, retrieval, agent workflow, MCP-style integration, evals, memory, tests, and deployment files.

## What should I be honest about?

This is a portfolio project, not a large production deployment. It uses local JSON storage and a simple sparse index for readability. The production version would use external databases, authentication, observability, and real model providers.
