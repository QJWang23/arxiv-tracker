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

    # Determine output path for returning
    if mode == "instant":
        report_path = REPORTS_DIR / "daily" / f"{date_str}-instant.md"
    else:
        week_num = datetime.now().isocalendar()[1]
        report_path = REPORTS_DIR / "weekly" / f"{datetime.now().year}-W{week_num:02d}.md"

    # Build the skill invocation command
    if mode == "instant":
        skill_cmd = f"/paper-analyzer --mode=instant --date={date_str}"
    else:
        week_num = datetime.now().isocalendar()[1]
        skill_cmd = f"/paper-analyzer --mode=weekly --week={datetime.now().year}-W{week_num:02d}"

    print(f"   Invoking: {skill_cmd}")

    # Run Claude CLI in non-interactive mode
    try:
        result = subprocess.run(
            ["claude", "-p", skill_cmd],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(Path(__file__).parent.parent),
        )

        if result.returncode == 0:
            print(f"   ✅ Deep analysis completed")
            if report_path.exists():
                return report_path
            print(f"   ⚠️ Report file not found at expected path: {report_path}")
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