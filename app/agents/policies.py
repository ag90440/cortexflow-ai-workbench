from typing import Dict

class PolicyGate:
    def assess(self, tool_name: str, arguments: Dict) -> Dict:
        risky_tools = {'create_ticket', 'memory_write'}
        risk = 'low'
        approval_required = False
        if tool_name in risky_tools:
            risk = 'medium'
        text = str(arguments).lower()
        if any(word in text for word in ['delete', 'payment', 'password', 'secret', 'production']):
            risk = 'high'
            approval_required = True
        if tool_name in risky_tools and 'approved' not in arguments:
            approval_required = approval_required or False
        return {'risk': risk, 'approval_required': approval_required, 'tool': tool_name}
