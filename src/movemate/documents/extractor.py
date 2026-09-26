from pydantic import BaseModel, Field

from movemate.domain.documents import DocumentFact


def extract_facts(text: str, source: str) -> list[DocumentFact]:
    """
    Extract structured facts from document text.

    The first version intentionally uses simple, deterministic
    extraction rules. LLM-based extraction can be introduced behind
    the same interface later.
    """
    facts: list[DocumentFact] = []

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines:
        if ":" not in line:
            continue

        field, value = line.split(":", 1)

        facts.append(
            DocumentFact(
                field=field.strip().lower(),
                value=value.strip(),
                confidence=1.0,
                source=source,
            )
        )

    return facts