# Model-routing playbook

## Why this exists
Your dashboard shows **18 of 32 sessions ran Opus 4.8, only 6 on Sonnet** (plus 4 Opus 4.7, 3 fable). For a design-build pipeline that ratio is inverted — most build work doesn't need Opus. Opus is the expensive, slow, deep-reasoning model; using it as the default is the single biggest avoidable cost in your workflow.

**Target ratio:** Sonnet as the default workhorse (~60–70% of sessions), Opus reserved for genuinely hard reasoning (~20–30%), Haiku for mechanical work. Roughly the *inverse* of where you are now.

## The three models, plainly
- **Haiku 4.5** — fast + cheapest. Mechanical, well-specified work. No judgment required.
- **Sonnet 4.6** — the workhorse. Builds, edits, applies an existing design system. Your default.
- **Opus 4.8** — deepest reasoning, slowest, priciest. Net-new design thinking, ambiguous structure, hard trade-offs.

## Route by pipeline step

| Step in your pipeline | Model | Why |
|---|---|---|
| Copy sweeps, find/replace, terminology fixes | **Haiku** | Mechanical text work |
| File/asset reorg, media-kit folder structure | **Haiku** | No judgment |
| Reading diffs / QA-checking what changed | **Haiku** | Verification, not creation |
| Status summaries, extracting content from a deck | **Haiku** | Low reasoning |
| Building a screen from an established pattern | **Sonnet** | Pattern application |
| figma-builder runs (DA→CL builds) | **Sonnet** | Mechanics already defined in the skill |
| Poster/asset layout from a clear brief | **Sonnet** | Execution of a known direction |
| Applying/extending an existing design system | **Sonnet** | System is the constraint |
| Most batched prompts in a DA→CL run | **Sonnet** | See PROMPT-BATCH-SOP.md |
| Net-new design exploration / ideation | **Opus** | Genuine creative reasoning |
| Dark-mode palette design from scratch | **Opus** | Systemic color reasoning (you already flagged this) |
| Restructuring a complex flow (e.g. loan detail) | **Opus** | Hard trade-offs |
| UX audit / journey mapping needing judgment | **Opus** | Evaluative reasoning |
| Ambiguous "figure out the right approach" tasks | **Opus** | Open-ended |

## The one rule, when in doubt
> Start in **Sonnet**. Escalate to **Opus only when Sonnet visibly struggles** — when the task is open-ended design thinking, not building something already decided. Drop to **Haiku** the moment the task is mechanical.

## Bake it in
- Each brand's `CLAUDE.md` carries a default-model line (already set to Sonnet).
- In a batched run, tag each prompt with its model (e.g. `[Sonnet]`, `[Opus]`) — your MMF run already did this well (10 Sonnet / 4 Opus). Make that the norm, not the exception.
- The "propose-before-build" gate (SOP) lets Opus do the *thinking* in one cheap step, then Sonnet does the *building* — instead of paying Opus rates for the whole job.

## What to watch on the dashboard
The model-mix doughnut is your scorecard. If Opus share trends down toward ~25–30% while output holds, the routing is working.
