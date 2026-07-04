# Learning Notes Used to Shape the Project

This project was shaped by the uploaded GenAI, Building LLM Applications, and expanded AI Engineer course pack. The goal was not to copy the content. The goal was to convert the learning themes into a working project.

## Style learned from the course material

The uploaded course material follows a useful pattern:

1. Explain the problem in simple language.
2. Show where the concept appears in real applications.
3. Break the architecture into small parts.
4. Add implementation steps.
5. Add a project that proves the concept.
6. Add traps, metrics, and interview framing.

CortexFlow applies the same structure through code and documentation.

## Concepts converted into code

| Course theme | Project decision |
|---|---|
| GenAI basics | Model router with local, Ollama, and OpenAI-compatible paths |
| Prompt and context engineering | Dedicated context engine with memory, evidence, and trace inputs |
| RAG | Document ingestion, chunking, sparse index, retrieval, citations |
| Vector databases | Local index that demonstrates ranking behavior before external DB swap |
| Tool use and function calling | Tool registry with schemas and structured execution |
| MCP | JSON-RPC tool, resource, and prompt interface |
| Agents | Planner, policy gate, tool executor, memory, reflection |
| Agent memory | Session events, long-term facts, memory search, versioning |
| Multi-agent systems | Planner, researcher, architect, critic, finalizer roles |
| LLM evaluation | RAG evaluation dataset and metrics |
| AI coding workflow | Code planning and review helper |
| ML system design | Blueprint generator for architecture and metrics |
| RL | Retrieval strategy bandit with reward updates |
| Fine-tuning | SFT and preference dataset export from traces |
| Computer-use agents | Safe simulated action planner |

## Why the project is different from a notes-only pack

The previous course pack was learning content. CortexFlow is an implementation artifact. It turns the concepts into endpoints, modules, tests, sample data, and a demo workflow.

## What was intentionally avoided

- No copied newsletter images inside the project repository.
- No copied article text.
- No previous project code reused.
- No code comments inside source files.
- No hidden API requirement for the core demo.
