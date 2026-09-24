from llama_index.core import Document


def test_llamaindex_document():
    document = Document(
        text="International residents may need to complete registration steps after arriving in Denmark."
    )

    assert document.text.startswith("International residents")