from typing import Dict, List

class SystemDesignBlueprint:
    def build(self, requirement: str) -> Dict:
        lowered = requirement.lower()
        workload = 'rag' if any(word in lowered for word in ['knowledge', 'policy', 'documents', 'search']) else 'agentic_app'
        risks = self._risks(lowered)
        return {
            'requirement': requirement,
            'workload': workload,
            'architecture': self._architecture(workload),
            'data_design': ['source connectors', 'document parser', 'metadata and permissions', 'chunk store', 'index refresh jobs'],
            'serving_design': ['FastAPI gateway', 'context engine', 'model router', 'tool executor', 'trace store'],
            'evaluation': ['golden dataset', 'groundedness', 'answer relevance', 'tool success rate', 'p95 latency', 'cost per task'],
            'safety': ['RBAC before retrieval', 'approval for write tools', 'secret masking', 'rate limits', 'audit logs'],
            'risks': risks,
            'first_milestone': 'ship a local demo with sample docs, traces, eval report, and one safe tool workflow'
        }

    def _architecture(self, workload: str) -> List[str]:
        if workload == 'rag':
            return ['ingestion', 'chunking', 'hybrid retrieval', 'reranking', 'context assembly', 'answer generation', 'evals', 'observability']
        return ['intent router', 'planner', 'tool registry', 'memory', 'policy gate', 'executor', 'critic', 'finalizer', 'observability']

    def _risks(self, text: str) -> List[str]:
        risks = ['stale context', 'hallucination', 'latency spikes', 'missing eval coverage']
        if any(word in text for word in ['delete', 'payment', 'update', 'approval']):
            risks.append('unsafe write action')
        if any(word in text for word in ['private', 'customer', 'employee', 'policy']):
            risks.append('permission leakage')
        return risks
