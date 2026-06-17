# Money Market Fund (MMF) — project context (CLAUDE.md)

## What this is
MMF investment app — light + dark themes. Work runs as batched DA->CL prompts (see PROMPT-BATCH-SOP.md).

## Company & decision-makers
- Company: Мони Маркет Фанд ХХК
- Deciders: the "MMF UX/UI" group (all leads in one Viber group)
- Feedback channel: Viber (group)

## Stack & design system
- Platform: TODO
- Design-system source: TODO
- Themes: mmf (light), mmf-dark
- Build skill: mmf-figma-builder

## Language & copy
- UI language: Mongolian (Cyrillic) — renders fine
- Terms to get right: Итгэлцэл (fund/trust term) vs Итгэмжлэл (authorization) — do NOT swap these; in onboarding_v2.jsx some "итгэмжлэл" near G-Sign copy may be intentional, verify before changing.

## Conventions & gotchas (observed)
- Secondary market is SELL-only — no buy order. Don't show a sale-order pill on the card.
- No "sun" icon next to wallet title — it has no purpose, remove.
- README historically says "no dark mode" — we ARE adding dark mode; override the README when you do.
- Home screen: 4 investment products should be visually prominent.
- Charts: "Сарын урсгал" x-axis = date, y-axis = MNT; loan payments shown in red.
- Education section (carousel → video/blog) must look visually distinct from the rest of the app.

## Assets
- Images: Magnific MCP (+ stock library)
- Figma: TODO
- Repo: TODO

## Default model
- Sonnet for the bulk of builds (copy sweeps, screen edits, batch conversions).
- Opus ONLY for: net-new exploration (home hero), dark-mode palette design, complex flow restructures.
