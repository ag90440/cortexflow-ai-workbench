# Project Walkthrough for GitHub and LinkedIn

## Demo goal

Show that CortexFlow is not a simple chatbot. It is a complete AI engineering system with multiple production concerns.

## Demo setup

Run:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run ui/streamlit_app.py
```

## Demo 1: RAG and citations

Question:

```text
How should RAG be evaluated?
```

What to show:

- Retrieved chunks
- Source ids
- Strategy used
- Latency
- Generated answer

What to say:

> I separated retrieval from generation so failures can be debugged. If the model gives a bad answer, I can inspect whether retrieval returned bad chunks or whether generation ignored good context.

## Demo 2: Agent workflow

Goal:

```text
Design a safe support agent with MCP tools and evaluation
```

What to show:

- Selected pattern
- Tool calls
- Policy gate
- Execution trace
- Reflection output
- Final answer

What to say:

> The model is not executing actions directly. It goes through a planner, a policy gate, and a typed tool registry. This is safer and easier to audit.

## Demo 3: MCP-style tools

Call:

```text
tools/list
```

What to show:

- Tool names
- Descriptions
- Input schemas
- Read-only flags

What to say:

> This demonstrates the idea that agents need a standard interface to tools, resources, and prompts instead of custom integrations hidden inside prompts.

## Demo 4: Multi-agent workflow

Objective:

```text
Design an enterprise policy Q&A assistant with evaluation and permissions
```

What to show:

- Planner output
- Researcher output
- Architect output
- Critic output
- Finalizer output
- Evaluation score

What to say:

> Multi-agent systems help when roles provide specialization, but they should not be used blindly because they add latency and coordination failure modes.

## Demo 5: EvalOps

Run the evaluation tab.

What to show:

- Overall score
- Expected term recall
- Token F1
- Groundedness
- Citation coverage
- Safety
- Latency

What to say:

> A production AI app should be evaluated with datasets and regression checks instead of only manual inspection.

## Demo 6: Fine-tuning data export

Run:

```bash
python scripts/export_sft_dataset.py --path data/runtime/sft.jsonl --mode sft
```

What to say:

> Traces can become training data only after filtering, privacy review, and quality checks. This project shows the export path without pretending every trace is automatically good training data.
