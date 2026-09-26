# MoveMate Denmark — Evaluation

## Purpose

The evaluation layer verifies that MoveMate's knowledge retrieval,
reasoning state, and task planning preserve the application's
grounding requirements.

The evaluation focuses on:

1. Retrieval relevance
2. Evidence grounding
3. Task dependency integrity
4. Prompt-injection handling

The evaluation intentionally avoids making live LLM calls during the
normal pytest suite. This keeps regression tests deterministic,
repeatable, and inexpensive.

## Retrieval Evaluation

The retrieval tests use the curated Denmark knowledge sources:

- Danish Tax Agency (Skattestyrelsen)
- Life in Denmark - ICS East in Copenhagen
- Life in Denmark - When You Arrive

Representative scenarios include:

- Tax-card questions for people moving to Denmark for work
- CPR-registration questions for non-EU residents moving to Copenhagen
- General settlement questions for international newcomers

The evaluation checks whether the expected authoritative source is
present in the retrieved evidence.

## Grounding Evaluation

MoveMate represents reasoning using structured `ReasoningResult`
objects.

The evaluation verifies that:

- proposed actions can reference only supplied evidence;
- task dependencies reference actions that actually exist;
- uncertainty can be represented without inventing unsupported actions;
- evidence and action relationships remain structurally valid.

The Gemini reasoning prompt additionally instructs the model not to
invent procedures, deadlines, eligibility requirements, documents,
appointments, or legal conclusions that are not supported by the
retrieved evidence.

## Prompt Injection

Retrieved content is treated as untrusted information.

The reasoning prompt explicitly instructs the model to ignore
instructions contained inside retrieved evidence.

Regression coverage verifies that malicious instructions are not
represented as application actions.

This is a defense-in-depth measure and is not a formal guarantee
against all prompt-injection attacks.

## Limitations

The current evaluation does not provide:

- statistically significant LLM benchmark scores;
- human-rated answer quality;
- automated semantic grading of every Gemini response;
- formal security guarantees;
- comprehensive Denmark-wide knowledge coverage.

The evaluation is intentionally small and focused on the MVP's
highest-risk behaviors: retrieval relevance, grounding, uncertainty,
and structured planning.

## Evaluation Status

The deterministic evaluation suite is executed as part of the
project's test suite.

Live Langfuse evaluation requires Langfuse credentials and is not
required for local application execution.