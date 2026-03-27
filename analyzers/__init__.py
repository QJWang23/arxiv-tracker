"""
Deep paper analyzer using Claude Code CLI.

Invokes the paper-analyzer skill via Claude CLI for Tier1 papers.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

REPORTS_DIR = Path(__file__).parent.parent / "reports"


def run_deep_analysis(mode: str, date_str: str = None) -> Optional[Path]:
    """
    Run deep analysis via Claude CLI paper-analyzer skill.

    Args:
        mode: "instant" for daily or "weekly" for weekly summary
        date_str: Date string (YYYY-MM-DD)

    Returns:
        Path to the generated report, or None if failed
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # Use separate path to avoid overwriting the basic report
    if mode == "instant":
        report_path = REPORTS_DIR / "daily" / f"{date_str}-deep.md"
    else:
        week_num = datetime.now().isocalendar()[1]
        report_path = REPORTS_DIR / "weekly" / f"{datetime.now().year}-W{week_num:02d}-deep.md"

    # Build the prompt - use natural language instead of slash command prefix
    # because `-p` mode may not correctly resolve `/skill-name` invocations
    if mode == "instant":
        prompt = (
            f"Analyze Tier1 papers from data/filtered/{date_str}.json. "
            f"Generate a deep analysis report in Chinese and save to {report_path}. "
            f"Follow the paper-analyzer skill's report template."
        )
    else:
        week_num = datetime.now().isocalendar()[1]
        week_str = f"{datetime.now().year}-W{week_num:02d}"
        prompt = (
            f"Analyze Tier1 papers from data/filtered/{date_str}.json for weekly summary {week_str}. "
            f"Generate a deep analysis report in Chinese and save to {report_path}. "
            f"Follow the paper-analyzer skill's report template."
        )

    print(f"   Running deep analysis (mode={mode}, date={date_str})...")
    print(f"   Output: {report_path}")

    # Run Claude CLI in non-interactive mode
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--allowed-tools", "Read,Write,Glob,Grep"],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(Path(__file__).parent.parent),
        )

        if result.returncode == 0:
            if report_path.exists():
                print(f"   ✅ Deep analysis report generated: {report_path}")
                return report_path
            # Report not at expected path - check if Claude generated it elsewhere
            print(f"   ⚠️ Report file not found at expected path: {report_path}")
            print(f"   Claude output (first 300 chars): {result.stdout[:300]}")
            return None
        else:
            stderr = result.stderr.strip() if result.stderr else ""
            stdout = result.stdout.strip() if result.stdout else ""
            print(f"   ❌ Claude CLI failed (returncode={result.returncode})")
            if stderr:
                print(f"   stderr: {stderr[:500]}")
            if stdout:
                print(f"   stdout: {stdout[:500]}")
            return None

    except subprocess.TimeoutExpired:
        print("   ❌ Deep analysis timed out (5 min)")
        return None
    except FileNotFoundError:
        print("   ❌ Claude CLI not found. Please install Claude Code.")
        return None
    except Exception as e:
        print(f"   ❌ Error running deep analysis: {e}")
        return None


def generate_deep_report(items: list, mode: str, date_str: str = None) -> Optional[Path]:
    """
    Entry point for deep analysis - calls Claude CLI.

    This function signature matches the original for compatibility with run.py.
    The items parameter is ignored as the skill reads from data/filtered/{date}.json
    """
    # Filter for Tier1 items to decide if we should run analysis
    tier1_count = sum(1 for item in items if item.get("keyword_tier") == "tier1_critical")

    if tier1_count == 0:
        print("   No Tier1 papers found, skipping deep analysis")
        return None

    print(f"   Found {tier1_count} Tier1 papers for deep analysis")

    return run_deep_analysis(mode, date_str)