from movemate.knowledge.embeddings import embed_text


def test_embed_text_returns_vector():
    vector = embed_text(
        "International residents may need to complete registration steps after arriving in Denmark."
    )

    assert isinstance(vector, list)
    assert len(vector) == 384
    assert all(isinstance(value, float) for value in vector)