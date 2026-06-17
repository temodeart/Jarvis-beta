# data.json schema (what the collector emits)

The collector merges three sources into one `data.json` the dashboard reads.

## Sources
1. **session_info** (in-app): `list_sessions` + `read_transcript`
   - AVAILABLE: session title, idle/running, cwd, is_child, tool/MCP calls (by name), errors/blocks (heuristic from transcript)
   - NOT AVAILABLE: token counts, per-turn model
2. **scheduled-tasks** (in-app): `list_scheduled_tasks` -> enabled, lastRunAt, nextRunAt (run health)
3. **registry.json + tasks.json** (manual + AI-written): projects, leads, the "needs me" hub
4. **(optional) Mac-local token script**: only path to real token/cost — reads ~/Library/Application Support/Claude session files. NOT reachable from the Cowork sandbox; must run on the Mac.

## Emitted shape
```json
{
  "generatedAt": "ISO",
  "projects": [{ "id","name","company","status","inFlight":0,"blocked":0,"lastActivity":"ISO" }],
  "sessions": [{ "id","title","project","state","mcpsUsed":[],"errors":[],"lastActivity":"ISO" }],
  "scheduled": [{ "id","desc","enabled","lastRunAt","nextRunAt","ok":true }],
  "tasksNeedingMe": [{ "id","project","title","owner" }],
  "usage": { "byModel": {}, "byMcp": {}, "tokens": null, "tokensSource": "unavailable|estimated|local-script" }
}
```
`usage.tokens` is `null` until the optional Mac-local script is wired in.
