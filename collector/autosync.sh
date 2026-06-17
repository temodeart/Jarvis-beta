#!/bin/bash
# Jarvis dashboard auto-refresh: regenerate data.json from Mac session files and push.
# Run on a schedule via launchd (see install block in SETUP.md). Safe to run anytime.
export PATH=/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin:$PATH
# self-locate the repo (works wherever the repo lives — keep it OUT of ~/Documents/Desktop/Downloads, which macOS blocks from background jobs)
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO" || exit 1
# clear any stale git locks left by interrupted operations
rm -f .git/index.lock .git/HEAD.lock .git/MERGE_HEAD .git/MERGE_MSG .git/objects/maintenance.lock 2>/dev/null
git fetch origin main -q || exit 1
git reset --hard origin/main -q            # match remote, discard local cruft
python3 collector/collect.py || exit 1     # writes docs/data.json from session files
git add docs/data.json
git -c user.email="temuujin.batb@gmail.com" -c user.name="temodeart" \
    commit -q -m "data: auto-refresh $(date '+%Y-%m-%d %H:%M')" || exit 0
git push origin main -q
