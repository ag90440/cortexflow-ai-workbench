from app.core.config import settings
from app.storage.json_store import JsonStore
import random

class RetrievalBandit:
    def __init__(self):
        self.arms = ['keyword', 'bm25', 'tfidf', 'hybrid']
        self.store = JsonStore(settings.runtime_dir / 'retrieval_bandit.json', {arm: {'pulls': 0, 'reward': 0.0} for arm in self.arms})

    def choose(self, epsilon: float = 0.1) -> str:
        data = self.store.read()
        if random.random() < epsilon:
            return random.choice(self.arms)
        scores = {arm: self._average(data.get(arm, {})) for arm in self.arms}
        return max(scores, key=scores.get)

    def update(self, arm: str, reward: float) -> dict:
        if arm not in self.arms:
            raise ValueError('unknown arm')
        data = self.store.read()
        row = data.setdefault(arm, {'pulls': 0, 'reward': 0.0})
        row['pulls'] += 1
        row['reward'] += float(reward)
        self.store.write(data)
        return {'arm': arm, 'average_reward': self._average(row), 'pulls': row['pulls']}

    def leaderboard(self) -> dict:
        data = self.store.read()
        return {arm: {'average_reward': self._average(data.get(arm, {})), 'pulls': data.get(arm, {}).get('pulls', 0)} for arm in self.arms}

    def _average(self, row: dict) -> float:
        pulls = row.get('pulls', 0)
        if pulls == 0:
            return 0.0
        return round(row.get('reward', 0.0) / pulls, 4)
