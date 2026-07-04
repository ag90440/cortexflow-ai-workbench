from app.agents.tools import ToolRegistry
from app.core.schemas import JsonRpcRequest, JsonRpcResponse
from app.rag.pipeline import RagPipeline
from typing import Dict

class LocalMcpServer:
    def __init__(self, registry: ToolRegistry, rag: RagPipeline):
        self.registry = registry
        self.rag = rag

    def handle(self, request: JsonRpcRequest) -> JsonRpcResponse:
        try:
            if request.method == 'initialize':
                return self._ok(request, {'server': 'cortexflow-local-mcp', 'version': '1.0.0', 'capabilities': ['tools', 'resources', 'prompts']})
            if request.method == 'tools/list':
                return self._ok(request, {'tools': self.registry.list_tools()})
            if request.method == 'tools/call':
                name = request.params.get('name', '')
                arguments = request.params.get('arguments', {})
                return self._ok(request, self.registry.execute(name, arguments))
            if request.method == 'resources/list':
                sources = sorted({item.get('source', '') for item in self.rag._load_chunks()})
                return self._ok(request, {'resources': [{'uri': f'kb://{source}', 'name': source} for source in sources]})
            if request.method == 'resources/read':
                uri = request.params.get('uri', '')
                source = uri.replace('kb://', '')
                chunks = [item for item in self.rag._load_chunks() if item.get('source') == source]
                return self._ok(request, {'uri': uri, 'text': '\n\n'.join(item.get('text', '') for item in chunks)})
            if request.method == 'prompts/list':
                return self._ok(request, {'prompts': [{'name': 'safe_agent', 'description': 'Agent prompt with retrieval, tool approval, and eval checks'}]})
            if request.method == 'prompts/get':
                return self._ok(request, {'name': 'safe_agent', 'messages': [{'role': 'system', 'content': 'Use approved tools, cite evidence, and stop when approval is required.'}]})
            return JsonRpcResponse(id=request.id, error={'code': -32601, 'message': 'method not found'})
        except Exception as exc:
            return JsonRpcResponse(id=request.id, error={'code': -32000, 'message': str(exc)})

    def _ok(self, request: JsonRpcRequest, result: Dict) -> JsonRpcResponse:
        return JsonRpcResponse(id=request.id, result=result)
