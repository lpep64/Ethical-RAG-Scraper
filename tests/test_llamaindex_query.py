import pytest
from rag_engine.llamaindex_query import answer_with_citations

def test_answer_with_citations_empty():
    answer, sources = answer_with_citations("")
    assert isinstance(answer, str)
    assert isinstance(sources, list)

def test_answer_with_citations_typical():
    question = "What is the most common tip?"
    answer, sources = answer_with_citations(question)
    assert isinstance(answer, str)
    assert isinstance(sources, list)
    # Optionally, check that sources are URLs
    for url in sources:
        assert url.startswith("https://")
