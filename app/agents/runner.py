from app.agents.patterns import PatternSelector, ReflectionEngine
from app.agents.planner import Planner
from app.agents.policies import PolicyGate
from app.agents.tools import ToolRegistry
from app.context.engine import ContextEngine
from app.core.schemas import AgentRequest, AgentResponse, AgentStep
from app.llm.providers import ModelRouter
from app.memory.store import MemoryStore
from typing import Dict, List
import time
import uuid

class AgentRunner:
    def __init__(self, registry: ToolRegistry, memory: MemoryStore):
        self.registry = registry
        self.memory = memory
        self.planner = Planner()
        self.policies = PolicyGate()
        self.patterns = PatternSelector()
        self.reflector = ReflectionEngine()
        self.context = ContextEngine()
        self.model = ModelRouter()

    def run(self, request: AgentRequest) -> AgentResponse:
        trace_id = str(uuid.uuid4())
        pattern = request.pattern if request.pattern != 'auto' else self.patterns.choose(request.goal)
        calls = self.planner.plan(request.goal)
        steps: List[AgentStep] = []
        tool_outputs: List[Dict] = []
        self.memory.add_event(request.session_id, 'user', request.goal, {'trace_id': trace_id})
        for index, call in enumerate(calls, start=1):
            assessment = self.policies.assess(call.name, call.arguments)
            if assessment['approval_required'] and not request.approved:
                step = AgentStep(step=index, role='policy', action=call.name, input=call.arguments, output=assessment, status='approval_needed')
                steps.append(step)
                continue
            output = self.registry.execute(call.name, call.arguments)
            tool_outputs.append({'tool': call.name, 'output': output})
            steps.append(AgentStep(step=index, role='executor', action=call.name, input=call.arguments, output=output, status='done' if output.get('ok') else 'skipped'))
        reflection = self.reflector.reflect(request.goal, [step.model_dump() for step in steps])
        messages = self.context.build(request.goal, [], self.memory.read_session(request.session_id), tool_outputs)
        final_answer = self.model.generate(messages)
        self.memory.add_event(request.session_id, 'assistant', final_answer, {'trace_id': trace_id, 'pattern': pattern})
        state = {'pattern': self.patterns.explain(pattern), 'reflection': reflection, 'tool_count': len(tool_outputs), 'created_at': time.time()}
        return AgentResponse(goal=request.goal, pattern=pattern, final_answer=final_answer, steps=steps, state=state, trace_id=trace_id)
