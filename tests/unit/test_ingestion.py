from pathlib import Path

from movemate.knowledge.ingestion import (
    create_chunks,
    extract_source_metadata,
    load_markdown,
)


def test_create_chunks_splits_paragraphs():
    text = "First paragraph.\n\nSecond paragraph."

    chunks = create_chunks(
        text=text,
        source_name="test-source",
        source_path="test.md",
    )

    assert len(chunks) == 2
    assert chunks[0].text == "First paragraph."
    assert chunks[1].text == "Second paragraph."


def test_load_markdown_reads_file():
    path = Path("data/sources/denmark-first-steps.md")

    text = load_markdown(path)

    assert "# First Steps When Coming to Denmark" in text

def test_create_chunks_preserves_source_url():
    chunks = create_chunks(
        text="Official registration information.",
        source_name="Life in Denmark",
        source_path="data/sources/address.md",
        source_url="https://lifeindenmark.borger.dk/example",
    )

    assert len(chunks) == 1
    assert chunks[0].source_url == "https://lifeindenmark.borger.dk/example"

def test_extract_source_metadata():
    text = """
# Example Source

## Source Metadata

Source name: Danish Tax Agency
Source URL: https://skat.dk/example
Topic: Registration
"""

    metadata = extract_source_metadata(text)

    assert metadata["source_name"] == "Danish Tax Agency"
    assert metadata["source_url"] == "https://skat.dk/example"