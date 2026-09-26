from qdrant_client.models import Distance, PointStruct, VectorParams
from uuid import uuid5, NAMESPACE_URL
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.embeddings import BaseEmbedding

from movemate.domain.models import Evidence, EvidenceType
from movemate.infrastructure.qdrant import qdrant_client
from movemate.knowledge.embeddings import embed_text


COLLECTION_NAME = "movemate_knowledge"
VECTOR_SIZE = 384


def ensure_collection() -> None:
    """
    Create the MoveMate knowledge collection if it does not already exist.
    """

    collections = qdrant_client.get_collections().collections
    collection_names = {collection.name for collection in collections}

    if COLLECTION_NAME not in collection_names:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

def reset_collection() -> None:
    """
    Delete the existing knowledge collection so it can be rebuilt
    from the current curated source files.
    """
    collections = qdrant_client.get_collections().collections
    collection_names = {collection.name for collection in collections}

    if COLLECTION_NAME in collection_names:
        qdrant_client.delete_collection(
            collection_name=COLLECTION_NAME,
        )


def index_chunk(
    chunk_id: str,
    text: str,
    source_name: str,
    source_path: str,
    source_url: str | None = None,
) -> None:
    """
    Embed one knowledge chunk and store it in Qdrant.
    """

    vector = embed_text(text)

    point_id = str(uuid5(NAMESPACE_URL, chunk_id))

    point = PointStruct(
    id=point_id,
    vector=vector,
    payload={
        "chunk_id": chunk_id,
        "text": text,
        "source_name": source_name,
        "source_path": source_path,
        "source_url": source_url,
    },
    )

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point],
    )


def search_knowledge(
    query: str,
    limit: int = 3,
) -> list[Evidence]:
    """
    Retrieve knowledge using LlamaIndex backed by Qdrant.

    Multiple retrieved chunks can belong to the same source document.
    Keep only the highest-scoring chunk for each source so downstream
    reasoning receives distinct evidence rather than duplicate sources.
    """

    index = get_llamaindex_index()

    retriever = index.as_retriever(
        similarity_top_k=limit,
    )

    nodes = retriever.retrieve(query)

    best_by_source: dict[str, Evidence] = {}

    for node in nodes:
        source_name = node.node.metadata["source_name"]

        evidence = Evidence(
            id=node.node.metadata["chunk_id"],
            evidence_type=EvidenceType.OFFICIAL,
            title=source_name,
            claim=node.node.get_content(),
            source_name=source_name,
            source_url=node.node.metadata.get("source_url"),
            confidence=node.score,
        )

        existing = best_by_source.get(source_name)

        if existing is None or (
            evidence.confidence is not None
            and (
                existing.confidence is None
                or evidence.confidence > existing.confidence
            )
        ):
            best_by_source[source_name] = evidence

    return list(best_by_source.values())

class FastEmbedAdapter(BaseEmbedding):
    """
    Adapts MoveMate's FastEmbed implementation to LlamaIndex's
    embedding interface.
    """

    model_name: str = "BAAI/bge-small-en-v1.5"

    def _get_text_embedding(self, text: str) -> list[float]:
        return embed_text(text)

    def _get_query_embedding(self, query: str) -> list[float]:
        return embed_text(query)

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)

def get_llamaindex_index() -> VectorStoreIndex:
    """
    Create a LlamaIndex index backed by the existing MoveMate
    Qdrant collection.
    """

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
    )

    embed_model = FastEmbedAdapter()

    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model,
    )


