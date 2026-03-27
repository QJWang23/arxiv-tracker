from typing import List, Dict, Set
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config_loader import get_tag_keywords


class Classifier:
    """Classify papers by domain tags."""

    def __init__(self):
        self.tag_keywords = get_tag_keywords()
        self._build_pattern_cache()

    def _build_pattern_cache(self):
        """Build lowercase keyword sets."""
        self.tag_patterns = {}
        for tag, keywords in self.tag_keywords.items():
            self.tag_patterns[tag] = [kw.lower() for kw in keywords]

    def classify(self, title: str, summary: str) -> List[str]:
        """Classify a paper into domain tags."""
        text = f"{title} {summary}".lower()
        tags = []

        for tag, keywords in self.tag_patterns.items():
            for kw in keywords:
                if kw in text:
                    tags.append(tag)
                    break  # Only add each tag once

        return tags

    def classify_item(self, item: dict) -> dict:
        """Add tags to an item dict."""
        tags = self.classify(
            item.get("title", ""),
            item.get("summary", "")
        )
        item["tags"] = tags
        return item


def classify_item(item: dict) -> List[str]:
    """Convenience function for classification."""
    clf = Classifier()
    return clf.classify(item.get("title", ""), item.get("summary", ""))
