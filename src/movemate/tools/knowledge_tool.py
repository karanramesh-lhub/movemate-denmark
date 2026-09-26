from movemate.domain.models import Evidence
from movemate.knowledge.retrieval import search_knowledge


def knowledge_search_tool(
    query: str,
    limit: int = 3,
) -> list[Evidence]:
    
    return search_knowledge(
        query=query,
        limit=limit,
    )