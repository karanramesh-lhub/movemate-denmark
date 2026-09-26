from pathlib import Path

from movemate.tools.document_tool import extract_document_facts


def test_extract_document_facts(tmp_path: Path):
    document = tmp_path / "employment_contract.txt"

    document.write_text(
        "Employer: Example Denmark A/S\n"
        "Job Title: Software Engineer\n"
        "Employment Start Date: 2026-11-01\n",
        encoding="utf-8",
    )

    facts = extract_document_facts(document)

    assert len(facts) == 3
    assert facts[0].field == "employer"
    assert facts[0].value == "Example Denmark A/S"
    assert facts[2].field == "employment start date"
    assert facts[2].value == "2026-11-01"