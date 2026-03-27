#!/usr/bin/env python3
"""
arXiv Paper Tracker - Main Entry Point

Usage:
    python run.py --mode=daily      # Daily collection and instant push
    python run.py --mode=weekly     # Weekly summary generation
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from collectors.arxiv_collector import collect_arxiv
from filters.keyword_filter import filter_by_keywords
from filters.classifier import Classifier
from filters.scorer import HeatScorer
from models import PaperItem
from notifiers.feishu import send_to_feishu, build_instant_card, build_weekly_card
from analyzers import generate_deep_report

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
FILTERED_DIR = DATA_DIR / "filtered"
REPORTS_DIR = BASE_DIR / "reports"


def collect_all_sources(days_back: int = 1) -> List[PaperItem]:
    """Collect from all configured sources."""
    print("📚 Collecting from arXiv...")
    items = collect_arxiv(days_back=days_back)
    print(f"   Found {len(items)} papers")
    return items


def filter_and_score(items: List[PaperItem]) -> List[Dict]:
    """Apply all filters and scoring."""
    print("🔍 Filtering and scoring...")

    # Convert to dicts
    item_dicts = [i.to_dict() for i in items]

    # Keyword filter
    filtered = filter_by_keywords(item_dicts)
    print(f"   After keyword filter: {len(filtered)}")

    # Classify
    clf = Classifier()
    for item in filtered:
        clf.classify_item(item)

    # Score
    scorer = HeatScorer()
    for item in filtered:
        scorer.score_item(item)

    # Sort by heat score
    filtered.sort(key=lambda x: x["heat_score"], reverse=True)

    return filtered


def save_filtered(items: List[Dict], date_str: str = None) -> Path:
    """Save filtered items to JSON."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    FILTERED_DIR.mkdir(parents=True, exist_ok=True)
    path = FILTERED_DIR / f"{date_str}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"💾 Saved filtered data to {path}")
    return path


def load_filtered_data(path: Path) -> List[Dict]:
    """Load filtered data from JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_hot_items(items: List[Dict]) -> List[Dict]:
    """Get items that should trigger instant push."""
    scorer = HeatScorer()
    hot = [
        item for item in items
        if scorer.should_instant_push(item["heat_score"], item["priority"])
    ]
    # Sort by priority (critical first) then by heat score
    priority_order = {"critical": 0, "high": 1, "normal": 2}
    hot.sort(key=lambda x: (priority_order.get(x["priority"], 3), -x["heat_score"]))
    return hot


def generate_report(items: List[Dict], mode: str, date_str: str = None) -> Path:
    """Generate markdown report (stub - actual analysis by Claude skill)."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    if mode == "instant":
        report_dir = REPORTS_DIR / "daily"
        filename = f"{date_str}-instant.md"
    else:
        week_num = datetime.now().isocalendar()[1]
        filename = f"{datetime.now().year}-W{week_num:02d}.md"
        report_dir = REPORTS_DIR / "weekly"

    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / filename

    # Generate basic report structure
    lines = [f"# {'即时推送' if mode == 'instant' else '周汇总'} - {date_str}\n"]

    for item in items:
        lines.append(f"## {item['title']}\n")
        lines.append(f"- **Source**: {item['source']}")
        lines.append(f"- **Heat Score**: {item['heat_score']}")
        lines.append(f"- **Priority**: {item['priority']}")
        lines.append(f"- **Tags**: {', '.join(item['tags'])}")
        lines.append(f"- **URL**: {item['url']}\n")
        lines.append(f"**Summary**: {item['summary'][:500]}...\n")
        lines.append("---\n")

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"📝 Generated report: {path}")
    return path


def main(mode: str, days_back: int = 1):
    """Main entry point."""
    print(f"🚀 arXiv Paper Tracker - {mode} mode\n")

    date_str = datetime.now().strftime("%Y-%m-%d")

    # Step 1: Collect
    items = collect_all_sources(days_back=days_back)

    if not items:
        print("No items collected. Exiting.")
        return

    # Step 2: Filter and score
    filtered = filter_and_score(items)

    if not filtered:
        print("No items passed filtering. Exiting.")
        return

    # Step 3: Save filtered data
    save_filtered(filtered, date_str)

    # Step 4: Process based on mode
    if mode == "daily":
        hot_items = filter_hot_items(filtered)
        if hot_items:
            print(f"🔥 {len(hot_items)} items qualify for instant push")
            report_path = generate_report(hot_items, "instant", date_str)

            # Deep analysis for Tier1 papers via Claude API
            print("\n🧠 Running deep analysis for Tier1 papers...")
            deep_report_path = generate_deep_report(filtered, "instant", date_str)

            # Send Feishu notification for each hot item
            for item in hot_items:
                card = build_instant_card(item, f"file://{report_path}")
                if send_to_feishu(card):
                    print(f"   ✅ Sent Feishu notification for: {item['title'][:50]}...")
                else:
                    print(f"   ❌ Failed to send Feishu notification")
        else:
            print("No items qualify for instant push today.")
    else:
        report_path = generate_report(filtered, "weekly")

        # Deep analysis for Tier1 papers via Claude API
        print("\n🧠 Running deep analysis for Tier1 papers...")
        deep_report_path = generate_deep_report(filtered, "weekly", date_str)

        # Build stats for weekly card
        stats = {
            "total": len(filtered),
            "categories": {}
        }
        for item in filtered:
            for tag in item.get("tags", []):
                stats["categories"][tag] = stats["categories"].get(tag, 0) + 1

        # Send Feishu notification for weekly summary
        card = build_weekly_card(stats, f"file://{report_path}")
        if send_to_feishu(card):
            print("   ✅ Sent weekly Feishu notification")
        else:
            print("   ❌ Failed to send weekly Feishu notification")

    print("\n✅ Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="arXiv Paper Tracker")
    parser.add_argument(
        "--mode",
        choices=["daily", "weekly"],
        default="daily",
        help="Run mode: daily (instant push) or weekly (summary)"
    )
    parser.add_argument(
        "--days-back",
        type=int,
        default=1,
        help="Number of days to look back for papers"
    )
    args = parser.parse_args()
    main(args.mode, args.days_back)
