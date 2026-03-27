# arXiv Paper Tracker

Automated paper tracking system for AI/LLM research with smart filtering and instant push notifications.

## Features

- **Multi-source collection**: arXiv, Semantic Scholar, GitHub, Hacker News
- **Smart filtering**: Keyword tiers, author watching, heat scoring
- **Deep analysis**: Claude-powered technical summaries for Tier1 papers
- **Instant push**: Critical papers sent immediately via Feishu
- **Auto archiving**: Reports automatically pushed to GitHub

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
export GITHUB_TOKEN="ghp_xxx"  # for GitHub archiving

# Run daily collection
python run.py --mode=daily

# Run weekly summary
python run.py --mode=weekly
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FEISHU_WEBHOOK_URL` | Yes | Feishu bot webhook for notifications |
| `GITHUB_TOKEN` | No | GitHub token for archiving reports |
| `SEMANTIC_SCHOLAR_API_KEY` | No | Semantic Scholar API key |

### Keyword Tiers

Edit `config/watchers.yaml` to customize your keyword tiers:

```yaml
arxiv_queries:
  keywords:
    tier1_critical:  # Highest priority - triggers deep analysis
      - "inference optimization"
      - "vLLM"
      - "KV cache"
    tier2_high:
      - "LLM serving"
      - "model quantization"
    tier3_normal:
      - "transformer"
```

## Project Structure

```
arxiv-tracker/
├── collectors/      # Data collection modules
├── filters/         # Filtering and scoring
├── analyzers/       # Deep analysis via Claude CLI
├── notifiers/       # Push notifications
├── scripts/         # Automation scripts
├── .claude/skills/  # Claude Code skills
│   └── paper-analyzer/
├── reports/         # Generated reports
│   ├── daily/       # {date}-instant.md, {date}-deep-analysis.md
│   └── weekly/      # {year}-W{week}.md
├── data/            # Cached data
└── config/          # Configuration files
```

## Usage

### Daily Mode

Collects papers from the past day, filters by keywords, and:
1. Identifies hot papers for instant push
2. Runs deep analysis for Tier1 papers
3. Sends Feishu notifications
4. Archives reports to GitHub

```bash
python run.py --mode=daily
```

### Weekly Mode

Generates a summary of all filtered papers from the past 7 days:
1. Collects and filters papers
2. Runs deep analysis for Tier1 papers
3. Sends weekly summary to Feishu
4. Archives reports to GitHub

```bash
python run.py --mode=weekly --days-back=7
```

## Deep Analysis

Deep analysis uses Claude Code CLI to generate detailed technical summaries for Tier1 (critical priority) papers.

### Prerequisites

Install Claude Code CLI:
```bash
# See: https://docs.anthropic.com/en/docs/claude-code
npm install -g @anthropic-ai/claude-code

# Authenticate
claude login
```

### Automatic Execution

Deep analysis runs automatically when:
- Daily/weekly script is executed
- At least one Tier1 paper is found (keyword_tier = "tier1_critical")

The `run.py` script invokes the `/paper-analyzer` skill via Claude CLI.

### Manual Execution

You can also run deep analysis manually:

```bash
# Via Python module
python -m analyzers.deep_analyzer --mode=instant --date=2026-03-27

# Or directly invoke the skill in Claude Code
/paper-analyzer --mode=instant --date=2026-03-27
```

### Analysis Output

Deep analysis generates reports with:
- Core technical points (preserving key terminology)
- Innovation highlights
- Impact on focus areas (inference optimization, K8s, hardware acceleration)
- Actionable follow-up points

## Automation

### Setup Cron Jobs

Cron jobs are configured for:
- **Daily**: 20:00 every day
- **Weekly**: 20:00 every Sunday

```bash
# View current crontab
crontab -l

# Logs are written to
/var/log/arxiv-tracker/daily.log
/var/log/arxiv-tracker/weekly.log
```

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/run_daily.sh` | Daily collection + notification + archiving |
| `scripts/run_weekly.sh` | Weekly summary + notification + archiving |
| `scripts/archive_to_github.sh` | Push reports to GitHub repository |

## Reports

### Output Locations

| Type | Path | Description |
|------|------|-------------|
| Daily basic | `reports/daily/{date}-instant.md` | Hot papers summary |
| Daily deep | `reports/daily/{date}-instant.md` | Tier1 deep analysis |
| Weekly | `reports/weekly/{year}-W{week}.md` | Weekly summary + deep analysis |
| Filtered data | `data/filtered/{date}.json` | Raw filtered paper data |

### GitHub Archiving

Reports are automatically committed and pushed to the configured GitHub repository when changes exist. The archive script:
1. Checks for changes in `reports/`
2. Commits with message: `chore: archive reports - {date}`
3. Pushes to `origin main`