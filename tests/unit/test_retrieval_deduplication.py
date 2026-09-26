from unittest.mock import MagicMock, patch

from movemate.knowledge.retrieval import search_knowledge


def test_search_knowledge_keeps_best_chunk_per_source():
    node_a1 = MagicMock()
    node_a1.node.metadata = {
        "chunk_id": "tax-1",
        "source_name": "Danish Tax Agency",
        "source_url": "https://example.com/tax",
    }
    node_a1.node.get_content.return_value = "Tax Agency chunk 1"
    node_a1.score = 0.90

    node_a2 = MagicMock()
    node_a2.node.metadata = {
        "chunk_id": "tax-2",
        "source_name": "Danish Tax Agency",
        "source_url": "https://example.com/tax",
    }
    node_a2.node.get_content.return_value = "Tax Agency chunk 2"
    node_a2.score = 0.70

    node_b = MagicMock()
    node_b.node.metadata = {
        "chunk_id": "ics-1",
        "source_name": "Life in Denmark - ICS East in Copenhagen",
        "source_url": "https://example.com/ics",
    }
    node_b.node.get_content.return_value = "ICS chunk"
    node_b.score = 0.80

    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = [
        node_a1,
        node_a2,
        node_b,
    ]

    mock_index = MagicMock()
    mock_index.as_retriever.return_value = mock_retriever

    with patch(
        "movemate.knowledge.retrieval.get_llamaindex_index",
        return_value=mock_index,
    ):
        results = search_knowledge(
            query="registration",
            limit=3,
        )

    assert len(results) == 2

    by_source = {item.source_name: item for item in results}

    assert by_source["Danish Tax Agency"].id == "tax-1"
    assert by_source["Danish Tax Agency"].confidence == 0.90

    assert (
        by_source["Life in Denmark - ICS East in Copenhagen"].id
        == "ics-1"
    )
