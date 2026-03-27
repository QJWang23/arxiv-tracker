import sys
import os

# Set required env vars before importing config_loader
os.environ.setdefault('SEMANTIC_SCHOLAR_API_KEY', 'test_key')
os.environ.setdefault('GITHUB_TOKEN', 'test_token')
os.environ.setdefault('FEISHU_WEBHOOK_URL', 'https://example.com/webhook')

sys.path.insert(0, '.')

from config_loader import load_config

def test_load_sources_config():
    config = load_config("sources")
    assert "arxiv" in config
    assert config["arxiv"]["base_url"] == "http://export.arxiv.org/api/query"

def test_load_watchers_config():
    config = load_config("watchers")
    assert "arxiv_queries" in config
    assert "cs.CL" in config["arxiv_queries"]["categories"]

def test_load_feishu_config():
    config = load_config("feishu")
    assert "webhook_url" in config