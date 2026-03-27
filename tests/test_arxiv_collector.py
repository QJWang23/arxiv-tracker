import sys
sys.path.insert(0, '.')

from collectors.arxiv_collector import build_query, parse_arxiv_entry


def test_build_query():
    query = build_query(["cs.CL", "cs.AI"], ["inference optimization", "quantization"])
    assert "cat:cs.CL" in query
    assert "cat:cs.AI" in query
    assert "inference optimization" in query


def test_parse_arxiv_entry():
    # Mock entry for testing
    class MockAuthor:
        name = "Test Author"

    class MockEntry:
        id = "http://arxiv.org/abs/2503.12345v1"
        title = "Test Paper Title"
        summary = "This is a test abstract."
        authors = [MockAuthor()]
        published = "2026-03-26T10:00:00Z"
        categories = []

    entry = MockEntry()
    item = parse_arxiv_entry(entry)
    assert item.source == "arxiv"
    assert item.id == "2503.12345"
    assert item.title == "Test Paper Title"
    assert "Test Author" in item.authors
