### Knowledge and Retrieval Layer

The knowledge layer is responsible for transforming authoritative source
documents into searchable evidence.

The responsibilities are separated into:

- `ingestion.py` — loads source documents and creates knowledge chunks.
- `embeddings.py` — converts text into vector embeddings.
- `retrieval.py` — performs semantic retrieval against Qdrant and converts
  retrieved content into domain-level `Evidence`.
- `sources.py` — represents and manages source metadata and provenance.

The agent interacts with the knowledge layer through a retrieval boundary
rather than directly depending on the embedding model or vector database.

This separation allows the embedding model or vector database implementation
to change without changing the agent orchestration layer.