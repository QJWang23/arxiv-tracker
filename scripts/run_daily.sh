#!/bin/bash
# Daily arXiv tracker runner
# Collects papers, filters, sends Feishu notification, and archives to GitHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="/var/log/arxiv-tracker/daily.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

log "========== Starting daily arXiv tracker =========="

cd "$PROJECT_DIR"

# Run the tracker
log "Running arXiv tracker in daily mode..."
if python run.py --mode=daily 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ Daily tracker completed successfully"
else
    log "❌ Daily tracker failed"
    exit 1
fi

# Archive to GitHub
log "Archiving reports to GitHub..."
if "$SCRIPT_DIR/archive_to_github.sh"; then
    log "✅ GitHub archive completed"
else
    log "⚠️ GitHub archive failed (non-critical)"
fi

log "========== Daily tracker finished =========="