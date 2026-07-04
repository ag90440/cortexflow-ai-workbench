from app.rag.pipeline import RagPipeline


def test_rag_returns_citations():
    rag = RagPipeline()
    response = rag.answer('What is RAG evaluation?', top_k=3)
    assert response.metrics['retrieved'] >= 1
    assert len(response.citations) >= 1
    assert response.answer
