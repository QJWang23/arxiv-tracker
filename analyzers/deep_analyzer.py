#!/usr/bin/env python3
"""
Deep Paper Analyzer - CLI Entry Point

Uses Claude Code CLI to invoke the paper-analyzer skill.

Usage:
    python -m analyzers.deep_analyzer --mode=instant --date=YYYY-MM-DD
    python -m analyzers.deep_analyzer --mode=weekly --date=YYYY-MM-DD
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from analyzers import run_deep_analysis


def main():
    parser = argparse.ArgumentParser(description="Deep Paper Analyzer (via Claude CLI)")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date to analyze (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--mode",
        choices=["instant", "weekly"],
        default="instant",
        help="Analysis mode: instant (daily) or weekly",
    )
    args = parser.parse_args()

    print(f"🔍 Deep Paper Analyzer - {args.mode} mode\n")
    print(f"   Date: {args.date}")

    # Run deep analysis via Claude CLI
    report_path = run_deep_analysis(args.mode, args.date)
    if report_path:
        print(f"\n✅ Deep analysis complete: {report_path}")
    else:
        print("\n⚠️ Deep analysis failed or no Tier1 papers found")


if __name__ == "__main__":
    main()