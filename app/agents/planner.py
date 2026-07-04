from app.core.schemas import ToolCall
from typing import List

class Planner:
    def plan(self, goal: str) -> List[ToolCall]:
        text = goal.lower()
        calls: List[ToolCall] = []
        if any(word in text for word in ['remember', 'save memory', 'store this']):
            calls.append(ToolCall(name='memory_write', arguments={'user_id': 'demo-user', 'text': goal}))
        if any(word in text for word in ['what', 'how', 'explain', 'rag', 'agent', 'mcp', 'policy', 'knowledge', 'search']):
            calls.append(ToolCall(name='search_knowledge', arguments={'query': goal, 'top_k': 4}))
        if any(word in text for word in ['calculate', 'sum', 'cost', 'latency']) and any(char.isdigit() for char in text):
            expression = ''.join(char for char in goal if char in '0123456789+-*/(). ')
            if expression.strip():
                calls.append(ToolCall(name='calculate', arguments={'expression': expression.strip()}))
        if any(word in text for word in ['ticket', 'incident', 'bug']):
            calls.append(ToolCall(name='create_ticket', arguments={'title': 'Agent generated ticket', 'body': goal, 'priority': 'medium'}))
        if any(word in text for word in ['design', 'architecture', 'system']):
            calls.append(ToolCall(name='system_design', arguments={'requirement': goal}))
        if any(word in text for word in ['review code', 'code review', 'test plan']):
            calls.append(ToolCall(name='code_review', arguments={'filename': 'input.txt', 'content': goal}))
        if any(word in text for word in ['browser', 'computer', 'click', 'screen']):
            calls.append(ToolCall(name='computer_use_plan', arguments={'task': goal}))
        calls.append(ToolCall(name='evaluate_answer', arguments={'answer': goal, 'reference': goal, 'contexts': [goal]}))
        return calls
