# MoveMate Denmark — Architecture Decisions

This document records the major architectural decisions made during development of MoveMate Denmark.

## ADR-001 — Use LangGraph for Agent Orchestration

**Status:** Accepted

Use LangGraph for the stateful reasoning workflow because the application has explicit stages, shared state, and conditional routing.

```text
START → analyze_profile → determine_information_needed
      → retrieve_evidence → reason_about_situation
      → build_task_plan → END
```

## ADR-002 — Separate Knowledge Retrieval from Agent Orchestration

**Status:** Accepted

LangGraph controls workflow; LlamaIndex and Qdrant handle knowledge retrieval.

```text
LangGraph → Knowledge Tool → LlamaIndex → Qdrant
```

## ADR-003 — Use Qdrant as the Vector Store

**Status:** Accepted

Qdrant provides local vector storage, similarity search, metadata, and Docker support.

## ADR-004 — Use FastEmbed for Local Embeddings

**Status:** Accepted

FastEmbed provides local, reproducible embeddings without a separate paid embedding API. The current collection uses 384-dimensional vectors.

Changing the embedding model requires rebuilding the collection.

## ADR-005 — Use PostgreSQL for Application State

**Status:** Accepted

PostgreSQL stores profiles, plans, and tasks.

```text
Qdrant → knowledge retrieval
PostgreSQL → application state
```

## ADR-006 — Use Structured Pydantic Models for Agent Output

**Status:** Accepted

Gemini output must match the Pydantic `ReasoningResult` schema. This provides validation for interpretation, evidence IDs, proposed actions, dependencies, uncertainty, and warnings.

## ADR-007 — Keep Evidence Grounding Explicit

**Status:** Accepted

Proposed actions should reference supplied evidence where appropriate. When evidence is insufficient, uncertainty is preserved rather than filling the gap with general knowledge.

## ADR-008 — Treat Retrieved Content as Untrusted Evidence

**Status:** Accepted

Retrieved content is data, not executable instructions. Prompt-injection regression tests provide defense in depth, not a formal security guarantee.

## ADR-009 — Use Deterministic Source-Level Evidence Deduplication

**Status:** Accepted

Multiple chunks from one source can dominate retrieval results. The retrieval layer keeps the highest-scoring result per source.

## ADR-010 — Use Deterministic Vector IDs

**Status:** Accepted

Vector IDs are generated deterministically from chunk IDs to prevent uncontrolled duplicates during repeated ingestion.

## ADR-011 — Add Document Facts as a Separate Domain Concept

**Status:** Accepted

User-provided document information is represented by `DocumentFact` and kept distinct from authoritative external evidence.

```text
Official evidence ≠ User-provided document fact
```

## ADR-012 — Use Simple Deterministic Document Extraction for the MVP

**Status:** Accepted

The MVP uses deterministic key/value extraction for text documents. PDF/OCR remain outside the MVP.

## ADR-013 — Use Streamlit for the MVP UI

**Status:** Accepted

Streamlit provides a fast demonstration interface. It communicates with FastAPI rather than directly accessing persistence or agent state.

## ADR-014 — Use Langfuse for AI Observability

**Status:** Accepted

Langfuse instruments planning requests, retrieval, and Gemini reasoning. The implementation records limited non-sensitive metadata.

## ADR-015 — Make Observability Non-Critical

**Status:** Accepted

MoveMate continues to function when Langfuse credentials are absent. External dashboard verification remains pending because no Langfuse project credentials are configured.

## ADR-016 — Use Environment-Based Configuration

**Status:** Accepted

Pydantic Settings and environment variables hold database URLs, service URLs, model settings, and secrets. `.env` is excluded from Git.

## ADR-017 — Add Explicit LLM Timeout and Service Errors

**Status:** Accepted

Gemini has an explicit client timeout. External LLM failures become `LLMServiceError`, and FastAPI returns HTTP 503 for unavailable reasoning. Malformed structured output is handled similarly.

## ADR-018 — Avoid a Multi-Agent Swarm for the MVP

**Status:** Accepted

One orchestrating LangGraph workflow is easier to understand, test, debug, evaluate, and demonstrate than a multi-agent swarm.

## ADR-019 — Keep the Knowledge Base Curated for the MVP

**Status:** Accepted

The MVP uses a small set of authoritative Denmark sources rather than attempting exhaustive Denmark-wide coverage.

## ADR-020 — Prefer Explicit Uncertainty Over Unsupported Completion

**Status:** Accepted

When evidence does not support a conclusion, MoveMate should state the uncertainty rather than invent a plausible answer. This intentionally results in fewer actions when evidence is weak.
