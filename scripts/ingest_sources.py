from pathlib import Path
import argparse

from movemate.knowledge.ingestion import (create_chunks,extract_source_metadata,load_markdown,)
from movemate.knowledge.retrieval import (ensure_collection,index_chunk,reset_collection,)


SOURCES_DIR = Path("data/sources")


def ingest_source(path: Path) -> int:
    text = load_markdown(path)
    metadata = extract_source_metadata(text)

    source_name = metadata.get("source_name", path.stem)
    source_url = metadata.get("source_url")

    chunks = create_chunks(
        text=text,
        source_name=source_name,
        source_path=str(path),
        source_url=source_url,
    )

    for chunk in chunks:
        index_chunk(
            chunk_id=chunk.chunk_id,
            text=chunk.text,
            source_name=chunk.source_name,
            source_path=chunk.source_path,
            source_url=chunk.source_url,
        )

    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest MoveMate knowledge sources into Qdrant."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the existing knowledge collection before ingestion.",
    )

    args = parser.parse_args()

    if args.reset:
        reset_collection()

    ensure_collection()

    source_files = sorted(SOURCES_DIR.glob("*.md"))

    total_chunks = 0

    for source_path in source_files:
        chunk_count = ingest_source(source_path)

        print(
            f"Ingested {source_path.name}: "
            f"{chunk_count} chunks"
        )

        total_chunks += chunk_count

    print(f"Total chunks ingested: {total_chunks}")


if __name__ == "__main__":
    main()