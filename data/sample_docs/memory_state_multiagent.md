# Memory, State, and Multi-Agent Systems

Memory stores facts that may be useful later. State tracks the current task, intermediate observations, selected tools, approvals, and final output. Consistency matters because an agent can otherwise act on stale or conflicting information.

Multi-agent systems split work across roles such as planner, researcher, architect, critic, and finalizer. They help when work benefits from specialization, but they add latency, cost, and coordination failure modes.

A strong multi-agent design has a shared task state, role boundaries, stopping criteria, trace logs, and an evaluator that decides whether the result is good enough.
