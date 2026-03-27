import sys
sys.path.insert(0, '.')

from filters.scorer import HeatScorer, calculate_heat_score


def test_scorer_init():
    scorer = HeatScorer()
    assert scorer.weights["citation_rate"] == 0.3
    assert scorer.weights["community_heat"] == 0.3


def test_calculate_basic_score():
    item = {
        "keyword_tier": "tier1_critical",
        "citation_count": 10,
        "hn_score": 100
    }
    score = calculate_heat_score(item)
    assert score > 0
    assert score <= 100


def test_tier_contribution():
    scorer = HeatScorer()
    tier_score = scorer._tier_score("tier1_critical")
    assert tier_score == 100

    tier_score = scorer._tier_score("tier2_high")
    assert tier_score == 70


def test_should_trigger_instant_push():
    scorer = HeatScorer()
    # High score with high priority
    assert scorer.should_instant_push(heat_score=85, priority="high") == True
    # High score but low priority
    assert scorer.should_instant_push(heat_score=85, priority="normal") == False
    # Low score
    assert scorer.should_instant_push(heat_score=70, priority="high") == False
