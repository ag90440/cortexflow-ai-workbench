from typing import Dict, List
import re

class CodingWorkflow:
    def build_plan(self, request: str) -> Dict:
        parts = [item.strip() for item in re.split(r'[\.;]', request) if item.strip()]
        tasks = parts or [request]
        return {
            'request': request,
            'steps': [
                {'name': 'clarify_scope', 'output': self._scope(request)},
                {'name': 'design_contracts', 'output': 'define inputs, outputs, error cases, and persistence'},
                {'name': 'write_tests_first', 'output': 'cover happy path, edge path, and failure path'},
                {'name': 'implement_small_patch', 'output': 'change one module at a time'},
                {'name': 'run_review_loop', 'output': 'check readability, security, latency, and rollback'}
            ],
            'task_breakdown': tasks
        }

    def review_text(self, filename: str, content: str) -> Dict:
        smells = []
        if len(content.splitlines()) > 220:
            smells.append('file is large and may need smaller modules')
        if 'eval(' in content or 'exec(' in content:
            smells.append('dynamic execution needs strong validation')
        if 'password' in content.lower() or 'secret' in content.lower():
            smells.append('possible secret handling risk')
        if not smells:
            smells.append('no obvious high-risk smell found')
        return {'filename': filename, 'smells': smells, 'test_ideas': ['unit test core logic', 'integration test API contract', 'regression test previous bug']}

    def _scope(self, request: str) -> str:
        if len(request) < 80:
            return 'small feature or focused bug fix'
        return 'larger change that should be split into milestones'
