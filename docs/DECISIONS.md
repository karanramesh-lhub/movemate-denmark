## ADR: Separate Embedding Generation from Retrieval

### Decision

Embedding generation is isolated from vector retrieval in a dedicated
`knowledge/embeddings.py` module.

### Context

MoveMate needs to convert source documents and user questions into vector
representations before performing semantic search.

Embedding generation and vector retrieval are different responsibilities.
Combining them would make the retrieval layer unnecessarily coupled to a
specific embedding implementation.

### Consequences

Positive:

- The embedding model can be changed independently.
- Retrieval remains responsible for search rather than model implementation.
- The agent does not depend directly on FastEmbed.
- Testing can verify embedding generation independently from Qdrant.
- The architecture remains easier to extend.

Trade-off:

- The knowledge layer contains one additional module.
- There is slightly more code and indirection.

### Current Implementation

FastEmbed is used for local embedding generation, with Qdrant used as the
vector store.