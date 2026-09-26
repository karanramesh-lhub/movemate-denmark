from dataclasses import dataclass
from pathlib import Path


@dataclass
class KnowledgeChunk:

    chunk_id: str
    text: str
    source_name: str
    source_path: str
    source_url: str | None = None


def load_markdown(path: Path) -> str:

    return path.read_text(encoding="utf-8")


def create_chunks(text: str,source_name: str,source_path: str,source_url: str | None = None,) -> list[KnowledgeChunk]:

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks: list[KnowledgeChunk] = []

    for index, paragraph in enumerate(paragraphs, start=1):
        chunks.append(
            KnowledgeChunk(
                chunk_id=f"{source_name}-{index}",
                text=paragraph,
                source_name=source_name,
                source_path=source_path,
                source_url=source_url,
            )
        )

    return chunks

def extract_source_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}

    for line in text.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if key == "source name":
            metadata["source_name"] = value
        elif key == "source url":
            metadata["source_url"] = value

    return metadata