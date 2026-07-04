from app.core.schemas import JsonRpcRequest
from app.dependencies import mcp_server


def test_mcp_lists_tools():
    response = mcp_server.handle(JsonRpcRequest(method='tools/list'))
    assert response.result is not None
    assert len(response.result['tools']) >= 3
