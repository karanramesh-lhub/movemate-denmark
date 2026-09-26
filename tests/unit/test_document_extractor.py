from movemate.documents.extractor import extract_facts



def test_extract_facts_from_key_value_document():
    text = """
    Employer: Example Denmark A/S
    Job Title: Software Engineer
    Employment Start Date: 2026-11-01
    Work Location: Copenhagen
    Contract Duration: 24 months
    """

    facts = extract_facts(
        text=text,
        source="employment_contract.txt",
    )

    assert len(facts) == 5

    assert facts[0].field == "employer"
    assert facts[0].value == "Example Denmark A/S"
    assert facts[0].confidence == 1.0
    assert facts[0].source == "employment_contract.txt"

    assert facts[2].field == "employment start date"
    assert facts[2].value == "2026-11-01"