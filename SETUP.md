# Phase A setup — collector + GitHub Pages dashboard

## One-time
```bash
# 1. Get the repo on your Mac (clone the empty repo, copy these files in)
cd ~/Developer            # or wherever you keep code
git clone https://github.com/temodeart/Jarvis-beta.git
# copy the contents of this command-center/ folder into Jarvis-beta/
#   Jarvis-beta/collector/  Jarvis-beta/docs/  Jarvis-beta/data/  Jarvis-beta/SETUP.md

# 2. First run — generates docs/data.json
cd Jarvis-beta
python3 collector/collect.py
#   -> prints sessions=NN models={...} tokens_found=true/false

# 3. Commit + push
git add . && git commit -m "Phase A: collector + dashboard" && git push

# 4. Enable GitHub Pages: repo Settings -> Pages -> Source: Deploy from branch
#    Branch: main, Folder: /docs -> Save.
#    Dashboard goes live at: https://temodeart.github.io/Jarvis-beta/
```

## Keep it fresh (pick one)
**launchd (recommended, every 3h):**
```bash
sed "s|REPLACE_WITH_REPO_PATH|$PWD|" collector/com.temo.jarvis.collector.plist \
  > ~/Library/LaunchAgents/com.temo.jarvis.collector.plist
launchctl load ~/Library/LaunchAgents/com.temo.jarvis.collector.plist
```
**or cron (every 3h):**
```bash
( crontab -l 2>/dev/null; echo "0 */3 * * * $PWD/collector/run-and-push.sh" ) | crontab -
```
**or manual:** `./collector/run-and-push.sh` whenever you want.

## Notes
- `collect.py` needs your GitHub push to be authenticated (it runs `git push` as you).
- Tokens: the collector scans `~/.claude` for Claude Code transcripts; if found you get real
  token totals, otherwise the dashboard shows model-mix as the cost proxy. Either way it works.
