from app.core.schemas import JsonRpcRequest
from app.mcp.server import LocalMcpServer
from typing import Dict
import uuid

class LocalMcpClient:
    def __init__(self, server: LocalMcpServer):
        self.server = server

    def call(self, method: str, params: Dict | None = None) -> Dict:
        request = JsonRpcRequest(id=str(uuid.uuid4()), method=method, params=params or {})
        response = self.server.handle(request)
        return response.model_dump()
