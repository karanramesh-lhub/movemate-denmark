from movemate.domain.models import Evidence, EvidenceType


def search_knowledge(query: str) -> list[Evidence]:
    return [
        Evidence(
            id="mock-evidence-001",
            evidence_type=EvidenceType.OFFICIAL,
            title="MoveMate sample knowledge",
            claim=f"Sample evidence retrieved for query: {query}",
            source_name="MoveMate test knowledge",
            confidence=1.0,
        )
    ]