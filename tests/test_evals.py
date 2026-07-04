from app.evals.metrics import expected_term_recall, groundedness, token_f1


def test_eval_metrics_are_bounded():
    assert 0 <= token_f1('rag uses retrieval', 'retrieval augmented generation') <= 1
    assert expected_term_recall('mcp tools resources prompts', ['tools', 'prompts']) == 1
    assert groundedness('rag retrieves context', ['rag retrieves private context']) > 0
