from movemate.knowledge.retrieval import search_knowledge


def test_copenhagen_non_eu_cpr_query_retrieves_ics_source():
    evidence = search_knowledge(
        (
            "I am a non-EU employee moving to Copenhagen. "
            "What do I need to know about CPR registration?"
        ),
        limit=5,
    )

    source_names = {item.source_name for item in evidence}

    assert "Life in Denmark - ICS East in Copenhagen" in source_names


def test_tax_card_query_retrieves_tax_source():
    evidence = search_knowledge(
        (
            "I am moving to Denmark for work. "
            "What should I know about a Danish tax card?"
        ),
        limit=5,
    )

    source_names = {item.source_name for item in evidence}

    assert "Danish Tax Agency (Skattestyrelsen)" in source_names


def test_arrival_query_retrieves_when_you_arrive_source():
    evidence = search_knowledge(
        (
            "What practical things should an international newcomer "
            "handle after arriving in Denmark?"
        ),
        limit=5,
    )

    source_names = {item.source_name for item in evidence}

    assert "Life in Denmark - When You Arrive" in source_names