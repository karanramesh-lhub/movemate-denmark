from movemate.tools.knowledge_tool import knowledge_search_tool


def test_knowledge_search_tool_returns_evidence():
    results = knowledge_search_tool(
        "registration after moving to Denmark"
    )

    assert results
    assert results[0].source_name == "registration"