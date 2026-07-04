from app.rl.bandit import RetrievalBandit


def test_bandit_updates_reward():
    bandit = RetrievalBandit()
    row = bandit.update('hybrid', 0.8)
    assert row['pulls'] >= 1
    assert 'hybrid' in bandit.leaderboard()
