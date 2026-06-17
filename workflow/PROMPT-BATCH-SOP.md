# Prompt-batch SOP (DA→CL workflow)

## What this is
You already do this brilliantly by hand in MMF — turning a messy list of change requests into a sequenced set of paste-ready prompts, each routed to the right model, with dependency ordering and a QA footer. This SOP makes it the standard so you stop reinventing it each time and stop babysitting the AI mid-build.

DA = the design agent (proposes/designs). CL = the build agent (implements in code). Most projects run DA→CL.

## The 6 steps

**1. Intake — dump every change item, unedited.**
Number them. Don't pre-merge or pre-solve. (Your MMF run started with 24 raw items.)

**2. Decompose into prompts P1…Pn.**
Each prompt = one atomic, self-contained change. One prompt should be QA-able on its own.

**3. Tag each prompt with a model.**
`[Haiku]` mechanical · `[Sonnet]` build · `[Opus]` net-new thinking. (See MODEL-ROUTING.md.) Aim for mostly Sonnet.

**4. Order by dependency.**
If item B references something item A creates, A runs first. *Example from MMF: the 4-digit PIN screen (P2) must exist before the prompts that reference the PIN step (items 5, 6, 13, 16).* Note dependencies explicitly at the top.

**5. Gate the expensive/ambiguous ones.**
For any prompt that involves a layout or direction choice, make it **"propose 2–3 directions and WAIT for my OK before building."** This lets Opus do the *thinking* cheaply, then Sonnet does the *building* — far cheaper than building the wrong thing and redoing it. (MMF P6/P8/P10 did exactly this.)

**6. End every prompt with the QA footer.**
> "List exactly what you changed — files touched and the lines/sections — so I can QA fast."

## Standard prompt template
```
[<model>] <Prompt title>

Context: <1–2 lines — which screen/component, current state>
Change: <the specific, bounded change>
Constraints: <brand rules, conventions — pull from CLAUDE.md>
<If a direction choice:> Propose 2–3 options and WAIT for my approval before building.

End: list exactly what you changed (files + lines).
```

## Shared QA checklist (paste at the bottom of every batch)
- [ ] Only the requested change was made — no scope creep
- [ ] Brand conventions respected (see CLAUDE.md gotchas)
- [ ] Copy/terminology correct (e.g. MMF: Итгэлцэл vs Итгэмжлэл)
- [ ] Light + dark both handled (where applicable)
- [ ] Changed files + lines listed
- [ ] No regressions in adjacent components

## Overrides
If a repo's README or convention contradicts the new work (MMF README said "no dark mode" while you were adding it), the prompt should **state the override AND update the README** so the next session doesn't fight you.

## Worked example (condensed from your MMF run)
24 raw items → **14 paste-ready prompts** → **10 Sonnet / 4 Opus**.
- Opus reserved for the 4 hard ones: loan-detail restructure, owned-product page redesign, home hero exploration, dark-mode palette.
- P1 (copy sweep, Haiku/Sonnet) + P2 (PIN screen) run first because later prompts depend on them.
- Dark mode is two-phase: Opus designs tokens + one proof screen → you approve → Sonnet converts the rest in 6 cheap batches.
That run is the reference implementation of this SOP.
