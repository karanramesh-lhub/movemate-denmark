from pathlib import Path

from movemate.knowledge.ingestion import create_chunks, load_markdown
from movemate.knowledge.retrieval import (
    ensure_collection,
    get_llamaindex_index,
    index_chunk,
    search_knowledge,
)


def test_knowledge_can_be_indexed_and_retrieved():
    source_path = Path("data/sources/denmark-first-steps.md")

    text = load_markdown(source_path)

    chunks = create_chunks(
        text=text,
        source_name="Danish Tax Agency (Skattestyrelsen)",
        source_path=str(source_path),
        source_url=(
            "https://skat.dk/en-us/individuals/"
            "cross-border-tax-matters/first-steps"
        ),
    )

    ensure_collection()

    for chunk in chunks:
        index_chunk(
            chunk_id=chunk.chunk_id,
            text=chunk.text,
            source_name=chunk.source_name,
            source_path=chunk.source_path,
            source_url=chunk.source_url,
        )

    results = search_knowledge(
        "I am moving to Denmark for employment. "
        "What registration information should I look into?"
    )

    assert results
    assert all(
        result.evidence_type.value == "official"
        for result in results
    )

    assert any(
        result.source_name == "Danish Tax Agency (Skattestyrelsen)"
        and result.source_url
        == (
            "https://skat.dk/en-us/individuals/"
            "cross-border-tax-matters/first-steps"
        )
        for result in results
    )

def test_llamaindex_can_use_existing_qdrant_collection():
    ensure_collection()

    index = get_llamaindex_index()

    assert index is not None


def test_search_knowledge_uses_llamaindex_retrieval():
    source_path = Path("data/sources/denmark-first-steps.md")

    text = load_markdown(source_path)

    chunks = create_chunks(
        text=text,
        source_name="Danish Tax Agency (Skattestyrelsen)",
        source_path=str(source_path),
        source_url=(
            "https://skat.dk/en-us/individuals/"
            "cross-border-tax-matters/first-steps"
        ),
    )

    ensure_collection()

    for chunk in chunks:
        index_chunk(
            chunk_id=chunk.chunk_id,
            text=chunk.text,
            source_name=chunk.source_name,
            source_path=chunk.source_path,
            source_url=chunk.source_url,
        )

    results = search_knowledge(
        "I am moving to Denmark for employment. "
        "What registration information should I look into?"
    )

    assert results

    assert any(
        result.source_name == "Danish Tax Agency (Skattestyrelsen)"
        for result in results
    )

    assert any(
        result.source_url
        == (
            "https://skat.dk/en-us/individuals/"
            "cross-border-tax-matters/first-steps"
        )
        for result in results
    )