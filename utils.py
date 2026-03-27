#!/usr/bin/env python3
"""
Utility functions for git operations and URL building.
"""

import subprocess
from pathlib import Path
from typing import Optional, List, Tuple


def get_repo_info() -> Tuple[str, str]:
    """
    Get GitHub repo base URL and current branch name from git remote.

    Returns:
        Tuple of (base_url, branch_name)
        e.g., ("https://github.com/user/repo", "main")

    Raises:
        RuntimeError: If not in a git repo or no remote configured
    """
    try:
        # Get remote URL
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()

        # Convert SSH URL to HTTPS URL
        # git@github.com:user/repo.git -> https://github.com/user/repo
        if remote_url.startswith("git@"):
            # SSH format: git@github.com:user/repo.git
            parts = remote_url.split(":")[1].replace(".git", "")
            base_url = f"https://github.com/{parts}"
        elif remote_url.startswith("https://"):
            # HTTPS format: https://github.com/user/repo.git
            base_url = remote_url.replace(".git", "")
        else:
            base_url = remote_url

        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        branch = result.stdout.strip() or "main"

        return base_url, branch

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to get git repo info: {e}")


def build_github_report_url(report_path: Path, base_url: str = None, branch: str = None) -> str:
    """
    Build a GitHub blob URL for a local report file.

    Args:
        report_path: Local path to the report file (absolute or relative)
        base_url: GitHub repo base URL (auto-detected if None)
        branch: Git branch name (auto-detected if None)

    Returns:
        Full GitHub URL like "https://github.com/user/repo/blob/main/reports/daily/2024-01-01.md"
    """
    if base_url is None or branch is None:
        base_url, branch = get_repo_info()

    # Get relative path from repo root
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())

        # Make report_path absolute if it isn't
        if not report_path.is_absolute():
            report_path = Path.cwd() / report_path

        relative_path = report_path.relative_to(repo_root)

    except (subprocess.CalledProcessError, ValueError):
        # Fallback: use the path as-is
        relative_path = report_path

    return f"{base_url}/blob/{branch}/{relative_path}"


def git_push_reports(files: List[Path], commit_message: str = None) -> bool:
    """
    Add, commit, and push report files to GitHub.

    Args:
        files: List of file paths to commit
        commit_message: Custom commit message (auto-generated if None)

    Returns:
        True if successful, False otherwise
    """
    if not files:
        return True

    try:
        # Filter to only existing files
        existing_files = [str(f) for f in files if f.exists()]
        if not existing_files:
            print("   No files to push")
            return True

        # Get repo root
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())

        # Generate commit message if not provided
        if commit_message is None:
            if len(existing_files) == 1:
                commit_message = f"docs: add report {Path(existing_files[0]).name}"
            else:
                commit_message = f"docs: add {len(existing_files)} reports"

        # Git add
        result = subprocess.run(
            ["git", "add"] + existing_files,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )

        # Git commit
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_root,
            capture_output=True,
            text=True
        )

        # Check if there was anything to commit
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print("   No changes to commit")
            return True

        result.check_returncode()

        # Git push
        result = subprocess.run(
            ["git", "push"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=60,
            check=True
        )

        print(f"   ✅ Pushed {len(existing_files)} report(s) to GitHub")
        return True

    except subprocess.CalledProcessError as e:
        stderr_msg = (e.stderr or "").strip()
        stdout_msg = (e.stdout or "").strip()
        cmd = e.cmd if hasattr(e, 'cmd') else "unknown"
        print(f"   ❌ Git push failed: cmd={cmd}")
        if stderr_msg:
            print(f"   stderr: {stderr_msg}")
        if stdout_msg:
            print(f"   stdout: {stdout_msg}")
        if not stderr_msg and not stdout_msg:
            print(f"   returncode: {e.returncode}")
        return False
    except Exception as e:
        print(f"   ❌ Git push error: {e}")
        return False