from pathlib import Path


def parse_text_file(path: str | Path) -> str:
    """
    Read a UTF-8 text-based document and return its contents.
    """
    document_path = Path(path)

    if not document_path.exists():
        raise FileNotFoundError(
            f"Document not found: {document_path}"
        )

    return document_path.read_text(encoding="utf-8")