import arxiv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import PaperItem
from config_loader import load_config

DATA_DIR = Path(__file__).parent.parent / "data" / "arxiv"


def build_query(categories: List[str], keywords: List[str]) -> str:
    """Build arXiv API query string."""
    cat_query = " OR ".join([f"cat:{c}" for c in categories])
    kw_query = " OR ".join([f'all:"{kw}"' for kw in keywords])
    return f"({cat_query}) AND ({kw_query})"


def parse_arxiv_entry(entry) -> PaperItem:
    """Parse arxiv entry into PaperItem."""
    # Extract arXiv ID from URL
    arxiv_id = entry.id.split("/abs/")[-1].split("v")[0]

    # Parse date
    date = datetime.fromisoformat(entry.published.replace("Z", "+00:00")).strftime("%Y-%m-%d")

    # Extract authors
    authors = [a.name for a in entry.authors]

    # Clean title
    title = re.sub(r'\s+', ' ', entry.title).strip()

    # Clean summary
    summary = re.sub(r'\s+', ' ', entry.summary).strip()

    return PaperItem(
        source="arxiv",
        id=arxiv_id,
        title=title,
        authors=authors,
        date=date,
        url=f"https://arxiv.org/abs/{arxiv_id}",
        summary=summary,
        tags=[],
        heat_score=0,
        priority="normal"
    )


def fetch_papers(max_results: int = 100, days_back: int = 1) -> List[PaperItem]:
    """Fetch recent papers from arXiv."""
    config = load_config("sources")
    watchers = load_config("watchers")

    categories = watchers["arxiv_queries"]["categories"]
    all_keywords = []
    for tier_kws in watchers["arxiv_queries"]["keywords"].values():
        all_keywords.extend(tier_kws)

    query = build_query(categories, all_keywords)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    items = []
    for result in search.results():
        item = parse_arxiv_entry(result)
        # Filter by date
        item_date = datetime.strptime(item.date, "%Y-%m-%d")
        cutoff = datetime.now() - __import__('datetime').timedelta(days=days_back)
        if item_date >= cutoff:
            items.append(item)

    return items


def save_papers(items: List[PaperItem], date_str: Optional[str] = None) -> Path:
    """Save papers to JSON file."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"{date_str}.json"

    data = [item.to_dict() for item in items]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return path


def collect_arxiv(days_back: int = 1) -> List[PaperItem]:
    """Main collection function."""
    items = fetch_papers(days_back=days_back)
    save_papers(items)
    return items