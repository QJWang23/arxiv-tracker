#!/bin/bash
# Weekly arXiv tracker runner
# Generates weekly summary, sends Feishu notification, and archives to GitHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="/var/log/arxiv-tracker/weekly.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

log "========== Starting weekly arXiv tracker =========="

cd "$PROJECT_DIR"

# Run the tracker (collect 7 days of papers for weekly summary)
log "Running arXiv tracker in weekly mode..."
if python run.py --mode=weekly --days-back=7 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ Weekly tracker completed successfully"
else
    log "❌ Weekly tracker failed"
    exit 1
fi

# Archive to GitHub
log "Archiving reports to GitHub..."
if "$SCRIPT_DIR/archive_to_github.sh"; then
    log "✅ GitHub archive completed"
else
    log "⚠️ GitHub archive failed (non-critical)"
fi

log "========== Weekly tracker finished =========="