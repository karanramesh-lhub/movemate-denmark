from movemate.knowledge.mock_retrieval import search_knowledge


def test_search_knowledge_returns_evidence():
    results = search_knowledge("registration")

    assert len(results) == 1
    assert results[0].evidence_type.value == "official"
    assert "registration" in results[0].claim