from pathlib import Path

import httpx
import streamlit as st

from movemate.documents.extractor import extract_facts
from movemate.domain.models import UserProfile


API_URL = "http://localhost:8000/api/v1/plan"


st.set_page_config(
    page_title="MoveMate Denmark",
    page_icon="M",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .movemate-header {
        text-align: center;
        padding: 0.5rem 0 1.5rem 0;
    }

    .movemate-title {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 0.25rem;
    }

    .movemate-subtitle {
        font-size: 1.05rem;
        opacity: 0.78;
    }

    .stButton > button {
        width: 100%;
        min-height: 2.8rem;
        border-radius: 0.65rem;
        font-weight: 600;
    }

    [data-testid="stFileUploader"] {
        border-radius: 0.75rem;
    }

    .fact-card {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 0.7rem;
        padding: 0.65rem 0.85rem;
        margin-bottom: 0.45rem;
    }

    .fact-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.65;
    }

    .fact-value {
        font-size: 0.95rem;
        margin-top: 0.1rem;
    }

    h1, h2, h3 {
        margin-top: 0.4rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="movemate-header">
        <div class="movemate-title">MoveMate Denmark</div>
        <div class="movemate-subtitle">
            Your agentic onboarding assistant for settling in Denmark
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Profile - two-column layout
# ---------------------------------------------------------------------------

st.subheader("Profile")

profile_col1, profile_col2 = st.columns(2, gap="large")

with profile_col1:
    name = st.text_input(
        "Name",
        placeholder="e.g. Alex",
    )

    nationality = st.text_input(
        "Nationality",
        placeholder="e.g. Indian",
    )

    residency_type = st.text_input(
        "Residency type",
        placeholder="e.g. Non-EU work permit",
    )

    destination_city = st.text_input(
        "Destination city",
        placeholder="e.g. Copenhagen",
    )

    arrival_date = st.date_input(
        "Arrival date",
        value=None,
    )

with profile_col2:
    employment_status = st.text_input(
        "Employment status",
        placeholder="e.g. Software Engineer",
    )

    employment_start_date = st.date_input(
        "Employment start date",
        value=None,
    )

    accommodation_type = st.text_input(
        "Accommodation",
        placeholder="e.g. Temporary apartment",
    )

    family_status = st.text_input(
        "Family status",
        placeholder="e.g. Single",
    )

    planned_stay_months = st.number_input(
        "Planned stay (months)",
        min_value=1,
        value=None,
        step=1,
        placeholder="e.g. 24",
    )


# ---------------------------------------------------------------------------
# Document facts - single column
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Document Facts")

uploaded_file = st.file_uploader(
    "Upload an employment or supporting document",
    type=["txt", "md"],
    help="For this MVP, text and Markdown documents are supported.",
)

document_facts = []

if uploaded_file is not None:
    try:
        document_text = uploaded_file.read().decode("utf-8")

        document_facts = extract_facts(
            document_text,
            source=uploaded_file.name,
        )

        if document_facts:
            st.success(
                f"Extracted {len(document_facts)} fact(s) "
                f"from {uploaded_file.name}."
            )

            for fact in document_facts:
                st.markdown(
                    f"""
                    <div class="fact-card">
                        <div class="fact-label">{fact.field}</div>
                        <div class="fact-value">{fact.value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(
                    f"Extraction confidence: {fact.confidence:.2f} "
                    f"· Source: {fact.source}"
                )
        else:
            st.info(
                "The document was read successfully, but no "
                "structured facts were extracted."
            )

    except UnicodeDecodeError:
        st.error(
            "The uploaded file could not be read as UTF-8 text."
        )


# ---------------------------------------------------------------------------
# Question - single column
# ---------------------------------------------------------------------------

st.divider()
st.subheader("What do you need help with?")

question = st.text_area(
    "Question",
    placeholder=(
        "Example: What should I do after arriving in Copenhagen "
        "to complete my initial registration?"
    ),
    height=110,
    label_visibility="collapsed",
)


# ---------------------------------------------------------------------------
# Generate plan
# ---------------------------------------------------------------------------

generate_plan = st.button(
    "Generate Personalized Plan",
    type="primary",
)


# ---------------------------------------------------------------------------
# API call and personalized plan - single column
# ---------------------------------------------------------------------------

if generate_plan:
    validation_errors = []

    if not nationality.strip():
        validation_errors.append("Nationality is required.")

    if not residency_type.strip():
        validation_errors.append("Residency type is required.")

    if not destination_city.strip():
        validation_errors.append("Destination city is required.")

    if not question.strip():
        validation_errors.append("Please enter a question.")

    if validation_errors:
        for error in validation_errors:
            st.error(error)
    else:
        profile = UserProfile(
            name=name.strip() or None,
            nationality=nationality.strip(),
            residency_type=residency_type.strip(),
            destination_city=destination_city.strip(),
            arrival_date=arrival_date,
            employment_start_date=employment_start_date,
            employment_status=employment_status.strip() or None,
            accommodation_type=accommodation_type.strip() or None,
            family_status=family_status.strip() or None,
            planned_stay_months=planned_stay_months,
        )

        payload = {
            "profile": profile.model_dump(mode="json"),
            "question": question.strip(),
            "document_facts": [
                fact.model_dump(mode="json")
                for fact in document_facts
            ],
        }

        with st.spinner(
            "Analyzing your situation and building your plan..."
        ):
            try:
                response = httpx.post(
                    API_URL,
                    json=payload,
                    timeout=120.0,
                )

                response.raise_for_status()
                result = response.json()

            except httpx.ConnectError:
                st.error(
                    "Could not connect to MoveMate API. "
                    "Make sure FastAPI is running on port 8000."
                )
                st.stop()

            except httpx.HTTPStatusError as exc:
                detail = "The planning request failed."

                try:
                    detail = exc.response.json().get(
                        "detail",
                        detail,
                    )
                except Exception:
                    pass

                st.error(
                    f"MoveMate returned an error "
                    f"({exc.response.status_code}): {detail}"
                )
                st.stop()

            except httpx.RequestError as exc:
                st.error(
                    f"Could not complete the request: {exc}"
                )
                st.stop()

        # -------------------------------------------------------------------
        # Personalized plan
        # -------------------------------------------------------------------

        st.divider()
        st.subheader("Personalized Plan")

        plan_id = result.get("plan_id")

        if plan_id:
            st.caption(f"Plan ID: {plan_id}")

        interpretation = result.get("interpretation")

        if interpretation:
            st.markdown("### Situation")

            with st.container(border=True):
                st.write(interpretation)

        tasks = result.get("tasks", [])

        st.markdown("### Tasks")

        if tasks:
            for index, task in enumerate(tasks, start=1):
                title = task.get(
                    "title",
                    f"Task {index}",
                )

                description = task.get(
                    "description",
                    "",
                )

                priority = task.get(
                    "priority",
                    "medium",
                )

                category = task.get(
                    "category",
                    "other",
                )

                status = task.get(
                    "status",
                    "pending",
                )

                dependencies = task.get(
                    "dependencies",
                    [],
                )

                with st.container(border=True):
                    st.markdown(f"**{index}. {title}**")

                    if description:
                        st.write(description)

                    st.caption(
                        f"Priority: {priority}  ·  "
                        f"Category: {category}  ·  "
                        f"Status: {status}"
                    )

                    if dependencies:
                        st.caption(
                            "Depends on: "
                            + ", ".join(dependencies)
                        )
        else:
            st.info(
                "No tasks were generated for this request."
            )

        evidence = result.get("evidence", [])

        if evidence:
            st.markdown("### Evidence")

            for item in evidence:
                with st.container(border=True):
                    st.markdown(
                        f"**{item.get('title', 'Evidence')}**"
                    )

                    st.write(
                        item.get(
                            "claim",
                            "",
                        )
                    )

                    source_name = item.get("source_name")
                    source_url = item.get("source_url")

                    if source_name:
                        st.caption(
                            f"Source: {source_name}"
                        )

                    if source_url:
                        st.caption(
                            f"URL: {source_url}"
                        )

        uncertainty = result.get("uncertainty", [])

        if uncertainty:
            st.markdown("### Uncertainty")

            for item in uncertainty:
                st.warning(item)

        warnings = result.get("warnings", [])

        if warnings:
            st.markdown("### Warnings")

            for item in warnings:
                st.warning(item)
