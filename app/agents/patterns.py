from typing import Dict, List

class PatternSelector:
    def choose(self, goal: str) -> str:
        text = goal.lower()
        if any(word in text for word in ['compare', 'evaluate', 'score', 'test']):
            return 'evaluator_optimizer'
        if any(word in text for word in ['research', 'design', 'architecture', 'plan']):
            return 'planner_executor'
        if any(word in text for word in ['tool', 'ticket', 'calculate', 'search']):
            return 'react_tool_loop'
        if any(word in text for word in ['multi', 'team', 'critic', 'review']):
            return 'multi_agent_debate'
        return 'router_then_answer'

    def explain(self, pattern: str) -> Dict:
        details = {
            'router_then_answer': 'route simple tasks directly to RAG or chat',
            'react_tool_loop': 'alternate reasoning, tool call, observation, and next step',
            'planner_executor': 'split objective into tasks, execute tools, then synthesize',
            'evaluator_optimizer': 'generate answer, score it, revise weak parts',
            'multi_agent_debate': 'use specialized roles for planning, research, critique, and finalization'
        }
        return {'pattern': pattern, 'why': details.get(pattern, details['router_then_answer'])}

class ReflectionEngine:
    def reflect(self, goal: str, steps: List[Dict]) -> Dict:
        missing = []
        if not any(step.get('action') == 'search_knowledge' for step in steps):
            missing.append('no retrieval step')
        if not any('eval' in step.get('action', '') for step in steps):
            missing.append('no evaluation step')
        if not missing:
            missing.append('trace has retrieval and evaluation coverage')
        return {'goal': goal, 'review': missing, 'ready': missing == ['trace has retrieval and evaluation coverage']}
