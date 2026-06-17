# Working with Temo — operating rules (memory)

## Hard rule: automation first, computer takeover LAST
When a task needs an external system (GitHub, etc.), the order of preference is:
1. A dedicated MCP / connector (search the registry; check if one can be added).
2. An API / CLI / script path.
3. A skill.
4. Only if none of the above exist: take over the browser/computer — and say so explicitly as a last resort.
Do NOT drive the user's browser/computer just because it's convenient. Look for the automated path first, every time. If unsure whether a connector exists, search the web and the registry before falling back.

## Context
- All work runs in Cowork (built on Claude Code) on one Mac, not always-on.
- GitHub repo: https://github.com/temodeart/Jarvis-beta (command center lives here).
- No GitHub connector is in the Anthropic registry; a custom MCP must be added manually (see SETUP/notes).
- Never ask Temo to paste secrets (tokens, PATs) into chat — they go into Terminal/config only.

## Projects (see data/registry.json)
Tino + Tino Go (Teso/SkyWhale), MMF (Мони Маркет Фанд, Viber group), Midas + CarMax (Telegram). Images via Magnific MCP.

## PROVEN: how I push to GitHub automatically (no user action)
The repo remote URL carries embedded auth and the sandbox can reach GitHub. Reliable pattern:
1. Read remote URL from the connected repo's .git/config.
2. `git clone <url>` into /tmp (sandbox-writable — the mounted folder blocks git's lock files, so never run git directly on the mount).
3. Apply file changes, commit, `git push origin main`.
This means: I produce files and ship them to GitHub myself. Temo does nothing. Verified on Phase A + Phase B.
Note: the user's local ~/Documents/Jarvis-beta is NOT the source of truth — GitHub is. Don't rely on the mounted copy's git state.
