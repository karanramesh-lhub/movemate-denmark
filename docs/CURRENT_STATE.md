# MoveMate Denmark — Current State

## Current Checkpoint

MoveMate Denmark has completed the core MVP implementation, PostgreSQL
persistence, document intelligence, evaluation coverage, and Langfuse
observability instrumentation.

The full automated test suite is currently green:

**54 tests passed.**

The remaining Starlette/AnyIO deprecation warning originates from the
installed third-party dependency and does not currently affect application
behavior.

## Working Architecture

```text
Streamlit UI
     |
     v
   FastAPI
     |
     v
 LangGraph Agent
     |
     +------------------------+
     |                        |
     v                        v
Knowledge Tool          Document Facts
     |                        |
     v                        |
LlamaIndex                    |
     |                        |
     v                        |
   Qdrant                     |
     |                        |
     +-----------+------------+
                 |
                 v
        Gemini Reasoning
                 |
                 v
           Task Planner
                 |
                 v
           PostgreSQL