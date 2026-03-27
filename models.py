from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json


@dataclass
class PaperItem:
    """Unified data model for all collected items."""
    source: str  # arxiv, github, nvidia_blog, hackernews
    id: str
    title: str
    authors: List[str]
    date: str
    url: str
    summary: str
    tags: List[str] = field(default_factory=list)
    heat_score: int = 0
    priority: str = "normal"  # normal, high, critical

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PaperItem":
        return cls(**d)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
