#!/usr/bin/env bash
# Refresh dashboard data and push to GitHub. Run from anywhere.
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$REPO/collector/collect.py" --push
