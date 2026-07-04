from app.core.schemas import AgentRequest
from app.dependencies import agent_runner


def test_agent_runs_tool_trace():
    response = agent_runner.run(AgentRequest(goal='Explain MCP tool use and evaluate the answer'))
    assert response.final_answer
    assert len(response.steps) >= 1
    assert response.state['tool_count'] >= 1
