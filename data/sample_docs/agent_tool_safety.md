# Agent Tool Safety

An AI agent combines a model, tools, memory, state, and policies. The model can request a tool call, but the backend should decide whether the call is allowed. Tool execution needs schemas, validation, scoped credentials, timeouts, retries, idempotency, and audit logs.

Read-only tools are safer than write tools. Write actions such as creating tickets, sending emails, updating records, deleting data, or making payments should require clear policies and sometimes human approval.

MCP style interfaces expose tools, resources, and prompts through a standard contract. This makes agent integrations easier to inspect, test, and govern.
