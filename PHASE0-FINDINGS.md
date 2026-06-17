# Phase 0 — Findings & Scaffold

## 1. Telemetry reality (verified)

| Question | Answer |
|---|---|
| Can the collector run from Claude's sandbox? | **No.** Your Mac's session files aren't mounted here. Collector runs either via the `session_info` tool inside a Cowork scheduled task, or as a script on your Mac. |
| Tasks, projects, in-flight/idle? | **Yes** — from `list_sessions`. |
| Which MCP/tool used where? | **Yes** — from transcript tool calls. |
| Blocked / errored agents? | **Yes (heuristic)** — e.g. I already spotted your `claude-fable-5` model error in the MMF session. |
| Scheduled-run health? | **Yes** — `lastRunAt`/`nextRunAt`/`enabled`. |
| Per-turn model? | **Not via the in-app path.** |
| **Token / cost numbers?** | **Not via the in-app path.** Only obtainable from a small script **on your Mac** reading `~/Library/Application Support/Claude/...`. Run `collector/token_usage_probe.sh` and paste me the output — that tells us if real cost numbers are feasible or if we estimate. |

**Bottom line:** the dashboard's task/visibility/MCP/blocked/scheduled layers are fully feasible with no infra. Token/cost is the one piece gated on the probe result + a tiny Mac-local helper.

## 2. Project registry (drafted — needs your correction)

Drafted `data/registry.json` from your sessions. Inferred groupings:
- **Sky whale** → Tino (superapp) + Tino Go (taxi mini app)
- **Мони Маркет Фанд ХХК** → Money Market Fund (light + dark)
- **Midas Finance** + **CarMax** → grouped (you build them together; confirm if same company)
- Cross-project: posters / media kits; internal: skill/pipeline development

Every `lead`, `leadChannel`, `repo`, and `figma` is marked `TODO` — those I can't infer. Fill them and the registry becomes the backbone for both the dashboard and the bot's routing.

## 3. Scaffold created

```
command-center/
├── PHASE0-FINDINGS.md         (this file)
├── data/
│   ├── registry.json          ← projects + leads (correct the TODOs)
│   ├── tasks.json             ← central "needs me" hub (seeded)
│   └── schema.md              ← what data.json will contain
├── collector/
│   └── token_usage_probe.sh   ← run on your Mac, paste output
└── dashboard/                 (built in Phase 1)
```

## 4. To finish Phase 0, I need from you

1. **Run `token_usage_probe.sh` on your Mac** and paste the output (decides real-vs-estimated cost).
2. **Fix the registry** — leads, channels, repos, and confirm whether CarMax = Midas's company.
3. **GitHub**: account/org name + repo name to create, and public or private?

Then Phase 1 (the live dashboard) starts.
