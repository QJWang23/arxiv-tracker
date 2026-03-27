import os
import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).parent / "config"


def load_config(name: str) -> dict:
    """Load a YAML config file by name (without .yaml extension)."""
    path = CONFIG_DIR / f"{name}.yaml"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Expand environment variables
    expanded = os.path.expandvars(content)
    return yaml.safe_load(expanded)


def get_watcher_authors() -> list:
    """Get list of watched authors/organizations."""
    config = load_config("watchers")
    return config.get("watchers", {}).get("authors", [])


def get_keyword_tiers() -> dict:
    """Get keyword tier configuration."""
    config = load_config("watchers")
    return config.get("arxiv_queries", {}).get("keywords", {})


def get_tag_keywords() -> dict:
    """Get tag-to-keywords mapping."""
    config = load_config("watchers")
    return config.get("tag_keywords", {})
