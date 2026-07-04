from app.core.schemas import AgentStep, MultiAgentRequest
from app.evals.metrics import groundedness, safety_score
from app.llm.providers import ModelRouter
from app.rag.pipeline import RagPipeline
from typing import Dict, List
import time
import uuid

class RoleAgent:
    def __init__(self, role: str):
        self.role = role
        self.model = ModelRouter()

    def run(self, objective: str, context: str) -> Dict:
        prompt = f'Role: {self.role}\nObjective: {objective}\nContext: {context}'
        answer = self.model.generate([{'role': 'system', 'content': f'Act as {self.role}.'}, {'role': 'user', 'content': prompt}])
        return {'role': self.role, 'answer': answer}

class MultiAgentCoordinator:
    def __init__(self, rag: RagPipeline):
        self.rag = rag
        self.roles = [RoleAgent('planner'), RoleAgent('researcher'), RoleAgent('architect'), RoleAgent('critic'), RoleAgent('finalizer')]

    def run(self, request: MultiAgentRequest) -> Dict:
        trace_id = str(uuid.uuid4())
        retrieved = self.rag.retrieve(request.objective, top_k=4)
        context = '\n'.join(item.get('text', '') for item in retrieved)
        outputs = []
        rolling = context
        for role in self.roles:
            result = role.run(request.objective, rolling)
            outputs.append(result)
            rolling += '\n' + result['answer']
        final = outputs[-1]['answer'] if outputs else ''
        report = {'groundedness': groundedness(final, [context]), 'safety': safety_score(final), 'roles': [item['role'] for item in outputs]}
        return {'trace_id': trace_id, 'objective': request.objective, 'outputs': outputs, 'final_answer': final, 'eval': report, 'created_at': time.time()}
