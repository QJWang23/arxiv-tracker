#!/bin/bash
# Archive reports to GitHub repository
# Usage: ./archive_to_github.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="/var/log/arxiv-tracker/github_archive.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Create log directory if needed
mkdir -p "$(dirname "$LOG_FILE")"

cd "$PROJECT_DIR"

# Check if there are changes to commit
if git diff --quiet reports/ && git diff --cached --quiet reports/; then
    log "No changes to archive"
    exit 0
fi

# Configure git user if not set
if [ -z "$(git config user.email)" ]; then
    git config user.email "arxiv-tracker@bot.local"
fi
if [ -z "$(git config user.name)" ]; then
    git config user.name "arxiv-tracker-bot"
fi

# Add and commit
DATE_STR=$(date '+%Y-%m-%d')
git add reports/
git commit -m "chore: archive reports - $DATE_STR"

# Push to remote
log "Pushing to GitHub..."
if git push origin main; then
    log "✅ Successfully archived reports to GitHub"
else
    log "❌ Failed to push to GitHub"
    exit 1
fi