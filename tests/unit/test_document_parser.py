from pathlib import Path

from movemate.documents.parser import parse_text_file


def test_parse_text_file(tmp_path: Path):
    document = tmp_path / "employment_contract.txt"

    document.write_text(
        "Employer: Example Denmark A/S\n"
        "Job Title: Software Engineer\n",
        encoding="utf-8",
    )

    text = parse_text_file(document)

    assert "Employer: Example Denmark A/S" in text
    assert "Job Title: Software Engineer" in text


def test_parse_text_file_raises_for_missing_file(tmp_path: Path):
    missing_document = tmp_path / "missing.txt"

    try:
        parse_text_file(missing_document)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass