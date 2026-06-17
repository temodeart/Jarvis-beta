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
