# CortexFlow Architecture Walkthrough

CortexFlow is organized like a small production AI platform. The code is split by responsibility so every AI engineering concept has a real implementation point.

## 1. API layer

The FastAPI layer exposes the application as a product, not only as scripts. It provides endpoints for chat, ingestion, RAG, agents, MCP, evaluation, RL strategy feedback, coding workflow, system design, and training dataset export.

Why this matters:

- AI features need APIs before they can be integrated into products.
- API boundaries force clear request and response schemas.
- Endpoints make the project easy to demo on GitHub and LinkedIn.

## 2. RAG layer

The RAG layer handles ingestion, chunking, retrieval, answer generation, and traces.

The important design decision is that retrieval and generation are separated. This is how production RAG should be explained in interviews. If the answer is wrong, you should know whether retrieval failed or generation failed.

Flow:

```text
source document -> chunks -> local index -> query -> retrieved chunks -> context -> model -> answer -> traces -> evals
```

## 3. Context engineering layer

The context engine decides what reaches the model. It combines:

- System instruction
- User goal
- Retrieved evidence
- Session memory
- Tool outputs
- Token budget limit

The model should not receive every possible piece of data. It should receive the smallest useful context that is allowed, relevant, recent, and safe.

## 4. Agent runtime

The agent runtime uses a controlled loop:

```text
goal -> planner -> policy gate -> tool executor -> memory update -> reflection -> final answer
```

This is intentionally safer than letting an LLM freely call tools. The model does not directly execute actions. The backend registry and policy gate control execution.

## 5. Tool registry

The tool registry is the central contract for agent capabilities. Every tool has:

- Name
- Description
- Input schema
- Read-only flag
- Handler
- Execution result
- Latency measurement

Implemented tools include knowledge search, calculator, memory read/write, ticket creation, answer evaluation, system design blueprint, code review, and computer-use planning.

## 6. MCP-style server

The MCP-style server exposes tools, resources, and prompts through JSON-RPC methods. It demonstrates the main idea behind modern AI tool ecosystems: agents should discover capabilities through a standard interface.

## 7. Memory and state

Memory is split into session events and long-term facts. Session memory helps the assistant understand the current conversation. Long-term memory stores useful facts by user.

State consistency is handled through versioned session events. Each new event increments the session version.

## 8. Multi-agent workflow

The multi-agent coordinator splits a complex objective across roles:

- Planner
- Researcher
- Architect
- Critic
- Finalizer

This shows specialization but also exposes the real tradeoff: multi-agent systems increase latency and coordination complexity.

## 9. EvalOps

The evaluation runner measures answers using transparent metrics. It reads sample evaluation cases, runs the RAG pipeline, and returns row-level and aggregate scores.

This is important because production LLM systems should not be shipped only by manually reading sample outputs.

## 10. RL strategy tuning

The RL module uses a simple epsilon-greedy bandit to choose among retrieval strategies. It is not meant to train a large model. It demonstrates the applied RL idea of actions, rewards, and policy improvement.

Actions are retrieval strategies. Rewards can come from eval score or user feedback.

## 11. Fine-tuning dataset export

The training module exports traces as supervised fine-tuning records or preference pairs. This demonstrates how production interaction logs can become training data after filtering and review.

## 12. UI and demo layer

The Streamlit UI lets viewers test the project without reading all code first. It is useful for LinkedIn demos, interviews, and GitHub screenshots.
