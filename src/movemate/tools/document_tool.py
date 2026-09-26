from pathlib import Path

from movemate.documents.extractor import DocumentFact, extract_facts
from movemate.documents.parser import parse_text_file


def extract_document_facts(path: str | Path) -> list[DocumentFact]:

    document_path = Path(path)

    text = parse_text_file(document_path)

    return extract_facts(
        text=text,
        source=document_path.name,
    )