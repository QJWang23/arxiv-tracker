import sys
sys.path.insert(0, '.')

from filters.keyword_filter import KeywordFilter, filter_by_keywords


def test_keyword_filter_init():
    kf = KeywordFilter()
    assert "tier1_critical" in kf.tiers
    assert "speculative decoding" in kf.tiers["tier1_critical"]


def test_match_tier():
    kf = KeywordFilter()
    title = "Flash Attention 2: Faster Attention with Better Parallelism"
    summary = "We present an improved attention mechanism."

    tier = kf.match_tier(title, summary)
    assert tier == "tier1_critical"


def test_filter_by_keywords():
    items = [
        {"title": "Flash Attention Paper", "summary": "Attention optimization", "id": "1"},
        {"title": "Generic ML Paper", "summary": "Machine learning basics", "id": "2"},
    ]
    filtered = filter_by_keywords(items)
    assert len(filtered) == 1
    assert filtered[0]["id"] == "1"


def test_assign_priority():
    kf = KeywordFilter()
    assert kf.assign_priority("tier1_critical") == "critical"
    assert kf.assign_priority("tier2_high") == "high"
    assert kf.assign_priority("tier3_normal") == "normal"
    assert kf.assign_priority(None) == "normal"
