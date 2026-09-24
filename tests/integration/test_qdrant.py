from movemate.infrastructure.qdrant import qdrant_client


def test_qdrant_connection():
    collections = qdrant_client.get_collections()

    assert collections is not None