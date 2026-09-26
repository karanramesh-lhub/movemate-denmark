MoveMate Denmark

MoveMate Denmark is an agentic AI assistant for international professionals moving to or settling in Denmark.

It combines profile-aware reasoning, authoritative knowledge retrieval, document fact extraction, dependency-aware task planning, persistence, and observability.

What the application does

A user provides:

personal and relocation profile information;

a question about settling in Denmark;

optionally, a supported text/Markdown document.

MoveMate then:

validates the request through FastAPI/Pydantic;

runs a LangGraph workflow;

retrieves relevant curated Denmark information through LlamaIndex and Qdrant;

extracts structured facts from uploaded documents;

sends the profile, evidence, and document facts to Gemini using structured output;

validates the LLM result with Pydantic;

converts proposed actions into deterministic Task objects;

preserves explicit dependencies, evidence references, and uncertainty;

persists the profile, plan, and tasks in PostgreSQL;

returns the plan to the Streamlit UI.

Architecture

Streamlit UI
     |
     v
   FastAPI
     |
     v
 LangGraph Agent
     |
     +-----------------------+
     |                       |
     v                       v
Knowledge Tool         Document Facts
     |
     v
 LlamaIndex
     |
     v
   Qdrant
     |
     +-----------+
                 |
                 v
        Gemini Reasoning
                 |
                 v
          Task Planner
                 |
                 v
            PostgreSQL

Langfuse -> optional AI observability

Responsibility boundaries

Component

Responsibility

Streamlit

Demonstration UI

FastAPI

HTTP API and request/response validation

LangGraph

Agent state and workflow orchestration

LlamaIndex

Retrieval abstraction

Qdrant

Vector storage and similarity search

FastEmbed

Text/query embeddings

Gemini

Grounded structured reasoning

Domain planner

Deterministic conversion from proposed actions to tasks

PostgreSQL

Application state and plan persistence

Langfuse

Optional AI observability

Pytest

Automated regression/evaluation

Docker Compose

Local PostgreSQL/Qdrant infrastructure

End-to-end execution chain

User
  |
  v
Streamlit
  |
  | POST /api/v1/plan
  v
FastAPI PlanRequest
  |
  v
graph.invoke()
  |
  v
LangGraph AgentState
  |
  +--> analyze_profile
  |
  +--> determine_information_needed
  |
  +--> retrieve_evidence
  |       |
  |       v
  |   knowledge_search_tool
  |       |
  |       v
  |   LlamaIndex retriever
  |       |
  |       v
  |   Qdrant similarity search
  |       |
  |       v
  |   Evidence[]
  |
  +--> reason_about_situation
  |       |
  |       v
  |   Gemini structured output
  |       |
  |       v
  |   ReasoningResult
  |
  +--> build_task_plan
          |
          v
      deterministic Task[]
          |
          v
         END
          |
          v
FastAPI receives final AgentState
  |
  v
save_plan()
  |
  v
SQLAlchemy
  |
  v
PostgreSQL
  |
  v
PlanResponse
  |
  v
Streamlit

Knowledge base

The MVP uses a small curated set of authoritative Denmark sources:

Danish Tax Agency (Skattestyrelsen)

Life in Denmark — When You Arrive

Life in Denmark — ICS East in Copenhagen

Knowledge is stored as chunks in Qdrant with source metadata and deterministic vector IDs.

To rebuild the knowledge collection:

uv run python scripts/ingest_sources.py --reset

The Qdrant service must be running first.

Document intelligence

The current MVP intentionally uses deterministic text extraction.

Supported formats:

.txt

.md

The extractor recognizes simple field: value lines and creates DocumentFact objects.

Example:

Employer: Example Denmark ApS
Position: Software Engineer
Employment start date: 2026-11-01
Work location: Copenhagen

PDF/OCR and complex document understanding are intentionally outside this MVP.

Local setup

Prerequisites

Python 3.11+

uv

Docker Desktop

Gemini API key for live reasoning

1. Install dependencies

uv sync

2. Configure environment

Copy:

.env.example

to:

.env

Set at least:

LLM_PROVIDER=gemini
LLM_API_KEY=<your Gemini API key>
LLM_MODEL=<your Gemini model>

Do not commit .env.

Langfuse keys are optional. The application continues to run without them.

3. Start infrastructure

docker compose up -d

This starts:

PostgreSQL on localhost:5432

Qdrant on localhost:6333

The FastAPI application creates the PostgreSQL tables during application startup.

4. Ingest knowledge

uv run python scripts/ingest_sources.py --reset

5. Start FastAPI

uv run uvicorn movemate.api.main:app --reload

Health check:

GET http://localhost:8000/health

Expected response:

{"status":"ok"}

6. Start Streamlit

In another terminal:

uv run streamlit run streamlit_app.py

The UI is available at:

http://localhost:8501

Testing

The repository contains unit, integration, retrieval, document, persistence, API, and evaluation tests.

The last verified local regression run before the final UI-only cleanup was:

54 passed

The test suite includes:

agent graph/routing tests;

domain model and task planner tests;

retrieval and LlamaIndex tests;

document parser/extractor tests;

API tests;

PostgreSQL repository tests;

Qdrant integration tests;

LLM client/grounding tests;

retrieval evaluation;

grounding/dependency evaluation;

prompt-injection regression.

Run the suite with:

uv run pytest -q

Use verbose output while debugging:

uv run pytest -v

Evaluation

The evaluation suite focuses on the highest-risk MVP behaviors:

retrieval relevance;

evidence grounding;

valid evidence references;

valid task dependencies;

uncertainty representation;

prompt-injection regression.

The evaluation does not claim that an LLM is always correct or that prompt injection is formally solved.

See:

docs/evaluation.md

Observability

Langfuse instrumentation covers:

planning requests;

retrieval;

Gemini reasoning.

Only limited metadata is recorded.

Langfuse is optional for local execution. External dashboard verification requires Langfuse project credentials.

Error handling and safety

The application includes:

Pydantic request validation;

explicit LLM timeout configuration;

LLMServiceError abstraction;

controlled HTTP 503 responses for unavailable reasoning;

structured LLM output validated by Pydantic;

evidence traceability requirements;

explicit uncertainty;

prompt-injection instructions treating retrieved content as data rather than instructions;

environment-based secret configuration.

Project structure

movemate-denmark/
├── README.md
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docs/
│   ├── BUILD_PLAN.md
│   ├── CURRENT_STATE.md
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   └── evaluation.md
├── data/
│   └── sources/
├── sample_docs/
├── scripts/
│   └── ingest_sources.py
├── src/
│   └── movemate/
│       ├── api/
│       ├── agent/
│       ├── documents/
│       ├── domain/
│       ├── infrastructure/
│       ├── knowledge/
│       ├── llm/
│       └── tools/
├── streamlit_app.py
└── tests/
    ├── unit/
    ├── integration/
    └── evaluation/

Deliberate MVP limitations

The current release does not implement:

immigration/legal advice engine;

tax calculator;

banking integration;

MitID integration;

Digital Post integration;

live government account access;

exhaustive Denmark-wide directory;

multi-agent swarm;

mobile application;

Kubernetes;

mandatory cloud deployment;

PDF/OCR;

comprehensive LLM benchmarking.

The knowledge base is intentionally small and curated for the MVP.

The current Evidence.confidence field contains a retrieval similarity score from the vector search and should not be interpreted as calibrated factual probability. Document extraction confidence is likewise a deterministic extraction signal, not a truth probability.

Design decisions

The main architectural decisions are documented in:

docs/DECISIONS.md

Important decisions include:

LangGraph for stateful orchestration;

LlamaIndex for retrieval rather than orchestration;

Qdrant for vector storage;

FastEmbed for lightweight local embeddings;

PostgreSQL for application state;

structured Gemini output;

deterministic task planning after LLM reasoning;

a single orchestrating agent rather than a multi-agent swarm;

curated authoritative sources for the MVP;

explicit uncertainty instead of unsupported completion.

License / project status

MoveMate Denmark is a portfolio/engineering MVP demonstrating an agentic AI architecture for relocation onboarding.

It is not a substitute for official Danish immigration, tax, municipal, or other professional advice. Users should verify consequential information against current official sources.