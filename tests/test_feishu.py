import sys
sys.path.insert(0, '.')

from notifiers.feishu import build_instant_card, build_weekly_card


def test_build_instant_card():
    item = {
        "title": "Test Paper",
        "summary": "This is a test abstract for the paper.",
        "url": "https://arxiv.org/abs/2503.12345",
        "heat_score": 85,
    }
    report_url = "https://github.com/user/repo/blob/main/reports/daily/2026-03-26.md"

    card = build_instant_card(item, report_url)

    assert card["msg_type"] == "interactive"
    assert "🚀" in card["card"]["header"]["title"]["content"]
    assert "Test Paper" in str(card)


def test_build_weekly_card():
    stats = {
        "total": 25,
        "categories": {
            "inference-opt": 10,
            "multimodal": 8,
            "architecture": 7,
        }
    }
    report_url = "https://github.com/user/repo/blob/main/reports/weekly/2026-W13.md"

    card = build_weekly_card(stats, report_url)

    assert card["msg_type"] == "interactive"
    assert "📊" in card["card"]["header"]["title"]["content"]
