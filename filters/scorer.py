from typing import Dict, Optional


class HeatScorer:
    """Calculate heat score for items."""

    # Weight configuration
    WEIGHTS = {
        "citation_rate": 0.3,
        "community_heat": 0.3,
        "author_influence": 0.2,
        "keyword_tier": 0.2,
    }

    # Tier score mapping
    TIER_SCORES = {
        "tier1_critical": 100,
        "tier2_high": 70,
        "tier3_normal": 40,
    }

    # Thresholds
    INSTANT_PUSH_THRESHOLD = 80

    def __init__(self, weights: Optional[Dict] = None):
        self.weights = weights or self.WEIGHTS.copy()

    def _tier_score(self, tier: Optional[str]) -> int:
        """Get score for keyword tier."""
        return self.TIER_SCORES.get(tier, 0)

    def _normalize(self, value: float, max_value: float) -> float:
        """Normalize value to 0-100 range."""
        if max_value <= 0:
            return 0
        return min(100, (value / max_value) * 100)

    def calculate(
        self,
        keyword_tier: Optional[str] = None,
        citation_count: int = 0,
        hn_score: int = 0,
        reddit_score: int = 0,
        author_influence: float = 0,
    ) -> int:
        """Calculate heat score (0-100)."""
        # Citation rate component (assume 100 citations = max)
        citation_score = self._normalize(citation_count, 100)

        # Community heat (HN + Reddit, assume 500 points = max)
        community_score = self._normalize(hn_score + reddit_score, 500)

        # Author influence (0-1 scale, normalized to 0-100)
        author_score = author_influence * 100

        # Keyword tier
        tier_score = self._tier_score(keyword_tier)

        # Weighted sum
        total = (
            self.weights["citation_rate"] * citation_score +
            self.weights["community_heat"] * community_score +
            self.weights["author_influence"] * author_score +
            self.weights["keyword_tier"] * tier_score
        )

        return int(round(total))

    def should_instant_push(self, heat_score: int, priority: str) -> bool:
        """Determine if item should trigger instant push."""
        return (
            heat_score > self.INSTANT_PUSH_THRESHOLD and
            priority in ["critical", "high"]
        )

    def score_item(self, item: dict) -> dict:
        """Add heat_score to item dict."""
        score = self.calculate(
            keyword_tier=item.get("keyword_tier"),
            citation_count=item.get("citation_count", 0),
            hn_score=item.get("hn_score", 0),
            reddit_score=item.get("reddit_score", 0),
            author_influence=item.get("author_influence", 0),
        )
        item["heat_score"] = score
        return item


def calculate_heat_score(item: dict) -> int:
    """Convenience function for scoring."""
    scorer = HeatScorer()
    return scorer.calculate(
        keyword_tier=item.get("keyword_tier"),
        citation_count=item.get("citation_count", 0),
        hn_score=item.get("hn_score", 0),
        reddit_score=item.get("reddit_score", 0),
        author_influence=item.get("author_influence", 0),
    )
