# MoveMate Denmark — Build Plan

## Project Goal

Build a production-oriented agentic AI assistant for international residents moving to or settling in Denmark.

The application should:
- understand a user's situation;
- retrieve relevant authoritative information;
- reason over the user's profile and evidence;
- produce a dependency-aware task plan;
- incorporate facts extracted from user documents;
- preserve uncertainty when evidence is insufficient;
- persist the resulting plan;
- expose the workflow through a simple UI;
- provide observability and evaluation coverage.

## 1. Foundation

- [x] Python project structure
- [x] `pyproject.toml`
- [x] `uv` dependency management
- [x] `.env.example`
- [x] `.gitignore`
- [x] Docker Compose
- [x] PostgreSQL container
- [x] Qdrant container
- [x] Pytest configuration
- [x] Development environment verification

## 2. Domain Model

- [x] `UserProfile`
- [x] `Task`
- [x] `TaskStatus`
- [x] `TaskCategory`
- [x] `TaskPriority`
- [x] `Evidence`
- [x] `EvidenceType`
- [x] `DocumentFact`
- [x] Structured validation using Pydantic

## 3. Knowledge and RAG

- [x] Curated Denmark knowledge sources
- [x] Source metadata
- [x] Markdown ingestion
- [x] Paragraph-based chunking
- [x] Metadata extraction
- [x] FastEmbed embeddings
- [x] Qdrant vector collection
- [x] LlamaIndex integration
- [x] Knowledge retrieval abstraction
- [x] Deterministic vector IDs
- [x] Source-level evidence deduplication
- [x] Knowledge ingestion script
- [x] Retrieval integration tests
- [x] Retrieval evaluation tests

Current curated sources:
- Danish Tax Agency (Skattestyrelsen)
- Life in Denmark — When You Arrive
- Life in Denmark — ICS East in Copenhagen

## 4. Agent Orchestration

- [x] `AgentState`
- [x] `ReasoningResult`
- [x] `ProposedAction`
- [x] Profile analysis node
- [x] Information-needed decision
- [x] Conditional graph routing
- [x] Knowledge retrieval node
- [x] Gemini reasoning node
- [x] Task planning node
- [x] LangGraph workflow
- [x] Explicit START/END graph wiring
- [x] Structured reasoning output
- [x] Evidence-grounded planning
- [x] Dependency validation
- [x] Uncertainty handling
- [x] Prompt-injection instructions

## 5. Document Intelligence

- [x] Text document parser
- [x] Deterministic key/value extraction
- [x] `DocumentFact` domain model
- [x] Document tool
- [x] Document facts included in agent state
- [x] Document facts passed to Gemini reasoning
- [x] Streamlit document upload
- [x] Document extraction tests
- [x] Document tool tests
- [x] End-to-end document-assisted planning

Not included in this MVP:
- [ ] PDF extraction
- [ ] OCR
- [ ] complex document classification

## 6. PostgreSQL Persistence

- [x] SQLAlchemy async configuration
- [x] PostgreSQL connection
- [x] Application database models
- [x] Profiles table
- [x] Plans table
- [x] Tasks table
- [x] Repository layer
- [x] Plan persistence
- [x] Plan retrieval
- [x] Async session handling
- [x] Windows/pytest event-loop-safe connection configuration
- [x] Repository integration tests

## 7. FastAPI

- [x] FastAPI application
- [x] Health endpoint
- [x] Planning endpoint
- [x] `PlanRequest`
- [x] `PlanResponse`
- [x] Pydantic request validation
- [x] Graph invocation
- [x] PostgreSQL persistence
- [x] Structured API response
- [x] Controlled LLM failure response
- [x] API integration tests

Planning endpoint: `POST /api/v1/plan`

## 8. Streamlit UI

- [x] Profile input
- [x] Question input
- [x] Document upload
- [x] Document fact extraction
- [x] FastAPI integration
- [x] Interpretation display
- [x] Task display
- [x] Evidence display
- [x] Uncertainty display
- [x] Warning display
- [x] Error handling
- [x] End-to-end UI verification

## 9. LLM Integration

- [x] Gemini client
- [x] Structured JSON output
- [x] Pydantic schema validation
- [x] Grounding instructions
- [x] Evidence traceability rules
- [x] Dependency validation rules
- [x] Prompt-injection handling instructions
- [x] LLM timeout configuration
- [x] LLM service error abstraction
- [x] Invalid structured-output handling
- [x] API-level 503 handling
- [x] LLM tests

## 10. Observability

- [x] Langfuse dependency
- [x] Langfuse configuration
- [x] Graceful no-credentials behavior
- [x] Planning request observation
- [x] Retrieval observation
- [x] Gemini generation observation
- [x] Non-sensitive observation metadata

External Langfuse dashboard verification remains pending because no Langfuse project credentials are configured.

## 11. Evaluation

- [x] Retrieval evaluation
- [x] Grounding structural evaluation
- [x] Evidence reference validation
- [x] Task dependency validation
- [x] Prompt-injection regression
- [x] Evaluation documentation

## 12. Production Hardening

- [x] Pydantic settings migration
- [x] Environment-based configuration
- [x] Langfuse configuration isolation
- [x] LLM timeout
- [x] LLM service exception abstraction
- [x] Invalid LLM response handling
- [x] Controlled API failure response
- [x] Input validation
- [x] Prompt-injection defenses
- [x] Secrets excluded from repository

Remaining terminology cleanup:
- [ ] Clearly distinguish retrieval similarity scores from factual confidence.
- [ ] Clearly distinguish deterministic document extraction confidence from factual truth.

## 13. Testing

Current full suite: **54 tests passed**

Coverage includes unit, integration, retrieval, document, persistence, API, reasoning, and evaluation behavior.

## 14. Documentation

- [x] Build plan
- [x] Current state
- [x] Evaluation documentation
- [x] Architecture documentation
- [x] Architecture decision records
- [ ] README production/demo documentation
- [ ] Final limitations review
- [ ] Final project structure review

## 15. Final Validation

- [ ] Final Docker/Qdrant/Postgres verification
- [ ] Start FastAPI
- [ ] Start Streamlit
- [ ] Execute normal planning scenario
- [ ] Execute document-assisted scenario
- [ ] Verify persisted plan
- [ ] Verify uncertainty behavior
- [ ] Verify evidence deduplication
- [ ] Verify API failure behavior
- [ ] Verify no secrets are tracked
- [ ] Review Git diff
- [ ] Commit final changes
- [ ] Push to GitHub

## 16. Explicitly Out of Scope

- immigration/legal advice engine
- tax calculator
- banking integration
- MitID integration
- Digital Post integration
- live government account access
- full Denmark-wide directory
- multi-agent swarm
- mobile application
- Kubernetes
- mandatory cloud deployment
- PDF/OCR
- comprehensive LLM benchmarking

## 17. Definition of Done

MoveMate is ready for submission when FastAPI, LangGraph, LlamaIndex, Qdrant, PostgreSQL, Gemini, document facts, Streamlit, observability instrumentation, evaluation coverage, error handling, environment configuration, automated tests, architecture documentation, README, final E2E regression, and GitHub submission are complete.
