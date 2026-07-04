from typing import Any, Callable, Dict, List
from app.agents.computer_use import ComputerUsePlanner
from app.coding.workflow import CodingWorkflow
from app.evals.metrics import groundedness, safety_score, token_f1
from app.memory.store import MemoryStore
from app.rag.pipeline import RagPipeline
from app.storage.json_store import JsonStore
from app.system_design.blueprints import SystemDesignBlueprint
from app.core.config import settings
import ast
import operator
import time
import uuid

class ToolRegistry:
    def __init__(self, rag: RagPipeline, memory: MemoryStore):
        self.rag = rag
        self.memory = memory
        self.ticket_store = JsonStore(settings.runtime_dir / 'tickets.json', [])
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_defaults()

    def list_tools(self) -> List[Dict[str, Any]]:
        return [{k: v for k, v in tool.items() if k != 'handler'} for tool in self.tools.values()]

    def execute(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self.tools:
            return {'ok': False, 'error': f'unknown tool {name}'}
        started = time.time()
        try:
            result = self.tools[name]['handler'](**arguments)
            return {'ok': True, 'tool': name, 'result': result, 'latency_ms': round((time.time() - started) * 1000, 2)}
        except Exception as exc:
            return {'ok': False, 'tool': name, 'error': str(exc), 'latency_ms': round((time.time() - started) * 1000, 2)}

    def _add(self, name: str, description: str, input_schema: Dict[str, Any], handler: Callable, read_only: bool = True) -> None:
        self.tools[name] = {'name': name, 'description': description, 'input_schema': input_schema, 'read_only': read_only, 'handler': handler}

    def _register_defaults(self) -> None:
        self._add('search_knowledge', 'Retrieve evidence from local knowledge base', {'query': 'string', 'top_k': 'integer'}, self.search_knowledge)
        self._add('calculate', 'Calculate safe arithmetic expressions', {'expression': 'string'}, self.calculate)
        self._add('memory_read', 'Read relevant long-term memory', {'user_id': 'string', 'query': 'string'}, self.memory_read)
        self._add('memory_write', 'Store useful long-term memory', {'user_id': 'string', 'text': 'string'}, self.memory_write, read_only=False)
        self._add('create_ticket', 'Create a simulated support ticket', {'title': 'string', 'body': 'string', 'priority': 'string'}, self.create_ticket, read_only=False)
        self._add('evaluate_answer', 'Score an answer against context and reference', {'answer': 'string', 'reference': 'string', 'contexts': 'array'}, self.evaluate_answer)
        self._add('system_design', 'Generate an AI system design blueprint', {'requirement': 'string'}, self.system_design)
        self._add('code_review', 'Review code text and propose test ideas', {'filename': 'string', 'content': 'string'}, self.code_review)
        self._add('computer_use_plan', 'Create a safe computer-use action plan', {'task': 'string'}, self.computer_use_plan)

    def search_knowledge(self, query: str, top_k: int = 5) -> Dict:
        rows = self.rag.retrieve(query, top_k=top_k)
        return {'query': query, 'matches': rows}

    def calculate(self, expression: str) -> Dict:
        value = SafeCalculator().calculate(expression)
        return {'expression': expression, 'value': value}

    def memory_read(self, user_id: str, query: str) -> Dict:
        return {'matches': self.memory.search(user_id, query)}

    def memory_write(self, user_id: str, text: str) -> Dict:
        return self.memory.remember_fact(user_id, text)

    def create_ticket(self, title: str, body: str, priority: str = 'medium') -> Dict:
        ticket = {'id': str(uuid.uuid4()), 'title': title, 'body': body, 'priority': priority, 'created_at': time.time(), 'status': 'open'}
        self.ticket_store.append(ticket)
        return ticket

    def evaluate_answer(self, answer: str, reference: str = '', contexts: List[str] | None = None) -> Dict:
        contexts = contexts or []
        return {'token_f1': token_f1(answer, reference), 'groundedness': groundedness(answer, contexts), 'safety': safety_score(answer)}

    def system_design(self, requirement: str) -> Dict:
        return SystemDesignBlueprint().build(requirement)

    def code_review(self, filename: str, content: str) -> Dict:
        return CodingWorkflow().review_text(filename, content)

    def computer_use_plan(self, task: str) -> Dict:
        return ComputerUsePlanner().plan(task)

class SafeCalculator:
    operators = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod, ast.USub: operator.neg}

    def calculate(self, expression: str) -> float:
        tree = ast.parse(expression, mode='eval')
        return self._eval(tree.body)

    def _eval(self, node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self.operators:
            return self.operators[type(node.op)](self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in self.operators:
            return self.operators[type(node.op)](self._eval(node.operand))
        raise ValueError('unsafe expression')
