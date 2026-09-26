from movemate.tools.knowledge_tool import knowledge_search_tool


def test_knowledge_search_tool_returns_evidence():
    results = knowledge_search_tool(
        "registration after moving to Denmark"
    )

    assert results

    assert all(
        result.evidence_type.value == "official"
        for result in results
    )

    assert all(
        result.source_name
        for result in results
    )

    assert all(
        result.source_url
        for result in results
    )