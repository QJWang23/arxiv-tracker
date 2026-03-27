from typing import List, Optional, Dict
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config_loader import get_keyword_tiers


class KeywordFilter:
    """Filter papers by keyword tiers."""

    def __init__(self):
        self.tiers = get_keyword_tiers()
        self._build_pattern_cache()

    def _build_pattern_cache(self):
        """Build lowercase keyword sets for fast matching."""
        self.tier_patterns = {}
        for tier, keywords in self.tiers.items():
            self.tier_patterns[tier] = [kw.lower() for kw in keywords]

    def match_tier(self, title: str, summary: str) -> Optional[str]:
        """Find the highest priority tier matching the paper."""
        text = f"{title} {summary}".lower()

        # Check tiers in priority order
        for tier in ["tier1_critical", "tier2_high", "tier3_normal"]:
            for kw in self.tier_patterns.get(tier, []):
                if kw in text:
                    return tier
        return None

    def assign_priority(self, tier: Optional[str]) -> str:
        """Map tier to priority level."""
        mapping = {
            "tier1_critical": "critical",
            "tier2_high": "high",
            "tier3_normal": "normal",
        }
        return mapping.get(tier, "normal")

    def filter(self, items: List[dict]) -> List[dict]:
        """Filter items and assign tiers/priorities."""
        filtered = []
        for item in items:
            tier = self.match_tier(item.get("title", ""), item.get("summary", ""))
            if tier:
                item["keyword_tier"] = tier
                item["priority"] = self.assign_priority(tier)
                filtered.append(item)
        return filtered


def filter_by_keywords(items: List[dict]) -> List[dict]:
    """Convenience function for filtering."""
    kf = KeywordFilter()
    return kf.filter(items)
