# MoveMate Denmark — Architecture

## 1. Overview

MoveMate Denmark is an agentic AI application that helps international residents understand and organize practical settlement tasks when moving to Denmark.

The system combines FastAPI, LangGraph, LlamaIndex, Qdrant, Gemini, PostgreSQL, Streamlit, and Langfuse.

## 2. High-Level Architecture

```text
                    Streamlit UI
                         |
                         v
                     FastAPI
                         |
                         v
                 LangGraph Agent
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
    Profile State   Knowledge Tool   Document Facts
                         |
                         v
                    LlamaIndex
                         |
                         v
                       Qdrant
                         |
                         v
                      Evidence
                         |
                         v
                 Gemini Reasoning
                         |
                         v
                    Task Planner
                         |
                         v
                    PostgreSQL
```

Langfuse provides observability around the planning request, knowledge retrieval, and Gemini reasoning operations when configured.

## 3. Request Flow

```text
1. User enters profile/question in Streamlit
                |
                v
2. Streamlit sends POST /api/v1/plan
                |
                v
3. FastAPI validates PlanRequest
                |
                v
4. LangGraph receives AgentState
                |
                v
5. Profile analysis
                |
                v
6. Determine whether information is required
                |
                +------ no ------> END
                |
               yes
                |
                v
7. Knowledge retrieval
                |
                v
8. Qdrant/LlamaIndex returns evidence
                |
                v
9. Gemini reasons over profile, question, evidence, document facts
                |
                v
10. Structured ReasoningResult
                |
                v
11. Task planner converts proposed actions into domain Task objects
                |
                v
12. Plan persisted to PostgreSQL
                |
                v
13. FastAPI returns PlanResponse
                |
                v
14. Streamlit displays interpretation, tasks, evidence, uncertainty, warnings
```

## 4. Repository Structure

```text
movemate-denmark/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── docs/
│   ├── BUILD_PLAN.md
│   ├── CURRENT_STATE.md
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   └── evaluation.md
├── src/
│   └── movemate/
│       ├── api/
│       ├── domain/
│       ├── agent/
│       ├── knowledge/
│       ├── documents/
│       ├── tools/
│       ├── infrastructure/
│       ├── llm/
│       └── config.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/
├── data/
│   └── sources/
├── sample_docs/
├── scripts/
└── streamlit_app.py
```

## 5. Component Responsibilities

### FastAPI
HTTP API, validation, response handling, API-level errors, and persistence orchestration.

### LangGraph
Workflow orchestration, shared agent state, conditional routing, and node execution.

### LlamaIndex
Knowledge retrieval integration and conversion of vector results into retrieval nodes/evidence.

### Qdrant
Vector storage and similarity search.

### Gemini
Interpretation, structured reasoning, evidence-backed actions, and uncertainty.

### PostgreSQL
Durable application state: profiles, plans, and tasks.

### Streamlit
Lightweight demonstration UI communicating with FastAPI over HTTP.

### Langfuse
AI observability for planning, retrieval, and generation when configured.

## 6. Agent State

```text
AgentState
├── user_profile
├── current_question
├── information_needed
├── document_facts
├── retrieved_evidence
├── reasoning_result
├── task_graph
├── completed_tasks
├── pending_tasks
├── decisions
├── warnings
└── final_response
```

## 7. Knowledge Pipeline

```text
Markdown source
      |
      v
Markdown loader
      |
      v
Paragraph chunking
      |
      v
Metadata extraction
      |
      v
FastEmbed
      |
      v
Qdrant
```

Retrieval:

```text
User question + profile context
            |
            v
       Qdrant/LlamaIndex
            |
            v
       Retrieved nodes
            |
            v
      Evidence objects
```

Evidence is deduplicated at the source level so multiple similar chunks from the same authoritative source do not overwhelm the reasoning context.

## 8. Reasoning and Grounding

Gemini receives:
1. user profile;
2. current question;
3. retrieved evidence;
4. extracted document facts.

It returns a structured `ReasoningResult` containing interpretation, evidence IDs, proposed actions, uncertainty, and warnings.

The reasoning prompt prevents invention of unsupported procedures, deadlines, eligibility, documents, offices, appointments, fees, and legal consequences.

## 9. Document Intelligence

```text
Uploaded document
       |
       v
UTF-8 parser
       |
       v
Key/value extractor
       |
       v
DocumentFact
       |
       v
AgentState
       |
       v
Gemini reasoning
```

PDF/OCR processing is outside the current MVP.

## 10. Persistence

```text
Profile
   |
   +--- Plan
          |
          +--- Task
```

Qdrant is responsible for vector retrieval; PostgreSQL is responsible for application persistence.

## 11. Observability

When configured:

```text
Planning Request
      |
      +---- Agent observation
      |
      +---- Retrieval observation
      |
      +---- Gemini generation observation
```

Only limited non-sensitive metadata is recorded.

## 12. Error Handling

External LLM failures become `LLMServiceError` and are translated by FastAPI into HTTP 503.

Malformed structured model output is treated as an LLM service failure.

Input validation is handled by Pydantic/FastAPI.

Unexpected programming errors are not silently swallowed.

## 13. Security Considerations

- environment-based secrets
- `.env` excluded from Git
- prompt-injection instructions
- structured output validation
- evidence traceability
- controlled external-service errors
- limited observability metadata

Retrieved knowledge is treated as untrusted content and as evidence rather than executable instructions.

## 14. Production-Oriented Design

Production-oriented means explicit boundaries, typed data, structured state, external-service isolation, timeouts, validation, persistence, observability, evaluation, tests, reproducibility, and documented limitations.

It does not mean the MVP is a fully deployed production service.

## 15. Known Limitations

The application intentionally does not implement live government accounts, immigration/legal advice, tax calculation, banking integration, MitID integration, Digital Post integration, complete Denmark-wide directory coverage, multi-agent swarm, mobile application, Kubernetes, mandatory cloud deployment, PDF/OCR, or comprehensive LLM benchmarking.

The knowledge base is intentionally small and curated for the demonstration journey.

Retrieval similarity scores are ranking signals, not calibrated probabilities of factual correctness.
