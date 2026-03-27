import sys
sys.path.insert(0, '.')

from models import PaperItem

def test_paper_item_creation():
    item = PaperItem(
        source="arxiv",
        id="2503.12345",
        title="Test Paper",
        authors=["Author One", "Author Two"],
        date="2026-03-26",
        url="https://arxiv.org/abs/2503.12345",
        summary="This is a test abstract.",
        tags=["inference-opt"],
        heat_score=0,
        priority="normal"
    )
    assert item.source == "arxiv"
    assert item.id == "2503.12345"
    assert item.priority == "normal"

def test_paper_item_to_dict():
    item = PaperItem(
        source="arxiv",
        id="2503.12345",
        title="Test Paper",
        authors=["Author One"],
        date="2026-03-26",
        url="https://arxiv.org/abs/2503.12345",
        summary="Abstract",
        tags=[],
        heat_score=50,
        priority="high"
    )
    d = item.to_dict()
    assert d["source"] == "arxiv"
    assert d["heat_score"] == 50

def test_paper_item_from_dict():
    d = {
        "source": "github",
        "id": "release-123",
        "title": "v1.0.0 Release",
        "authors": ["Kubernetes"],
        "date": "2026-03-26",
        "url": "https://github.com/...",
        "summary": "Release notes",
        "tags": ["k8s-infra"],
        "heat_score": 30,
        "priority": "normal"
    }
    item = PaperItem.from_dict(d)
    assert item.source == "github"
    assert item.tags == ["k8s-infra"]
