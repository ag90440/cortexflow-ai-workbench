from typing import Dict, List

class ComputerUsePlanner:
    def plan(self, task: str) -> Dict:
        lowered = task.lower()
        actions = []
        actions.append({'type': 'observe', 'target': 'screen', 'reason': 'understand current UI state before acting'})
        if any(word in lowered for word in ['browser', 'website', 'page', 'form']):
            actions.append({'type': 'navigate', 'target': 'requested page', 'reason': 'open the required workspace'})
        if any(word in lowered for word in ['search', 'find', 'lookup']):
            actions.append({'type': 'type', 'target': 'search input', 'reason': 'enter the query exactly'})
            actions.append({'type': 'click', 'target': 'search or submit button', 'reason': 'execute the query'})
        if any(word in lowered for word in ['download', 'delete', 'send', 'submit', 'pay']):
            actions.append({'type': 'approval_required', 'target': 'human', 'reason': 'the requested action may change state or expose data'})
        actions.append({'type': 'verify', 'target': 'result screen', 'reason': 'check that the observed result matches the goal'})
        return {'task': task, 'mode': 'simulated_safe_plan', 'actions': actions, 'guardrails': ['no credential entry', 'no irreversible action without approval', 'record observation after every action']}
