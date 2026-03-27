# arXiv Paper Tracker

Automated paper tracking system for AI/LLM research with smart filtering and instant push notifications.

## Features

- **Multi-source collection**: arXiv, Semantic Scholar, GitHub, Hacker News
- **Smart filtering**: Keyword tiers, author watching, heat scoring
- **Deep analysis**: Claude-powered technical summaries
- **Instant push**: Critical papers sent immediately via Feishu

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run daily collection
python run.py --mode=daily

# Run weekly summary
python run.py --mode=weekly
```

## Configuration

1. Set environment variables:
   - `SEMANTIC_SCHOLAR_API_KEY` (optional)
   - `GITHUB_TOKEN` (optional, for higher rate limits)
   - `FEISHU_WEBHOOK_URL` (for notifications)

2. Customize `config/watchers.yaml` with your interests:
   - Keywords in `arxiv_queries.keywords`
   - Authors/organizations in `watchers.authors`

## Project Structure

```
arxiv-tracker/
├── collectors/      # Data collection modules
├── filters/         # Filtering and scoring
├── notifiers/       # Push notifications
├── skills/          # Claude skill definitions
├── reports/         # Generated reports
├── data/            # Cached data
└── config/          # Configuration files
```

## Usage

### Daily Mode
Collects papers, filters by keywords, and identifies papers for instant push.

```bash
python run.py --mode=daily
```

### Weekly Mode
Generates a summary of all filtered papers from the past week.

```bash
python run.py --mode=weekly
```

### Claude Skill Analysis
After running the collection, use the Claude skill for deep analysis:

```
/paper-analyzer --mode=instant --date=2026-03-26
```
