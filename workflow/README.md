# Workflow hardening (Phase B)

Three pieces, in build order:
1. **brand-memory/** — a `CLAUDE.md` per brand. Place each at the ROOT of that brand's repo. Cowork/Claude Code auto-loads `CLAUDE.md` from the working folder, so every session in that repo starts already knowing the brand. Fixes "repeating myself".
2. **MODEL-ROUTING.md** — which model for which step. Fixes cost (your sessions ran 18 Opus vs 6 Sonnet — inverted from ideal).
3. **PROMPT-BATCH-SOP.md** — standardizes the batched DA->CL workflow you already do by hand in MMF. Fixes manual back-and-forth.

## How memory is split
- `CLAUDE.md` (repo root) = brand CONTEXT: who decides, voice, palette, language, conventions, gotchas, default model.
- `*-figma-builder` skill = build MECHANICS: tokens, bundle contract, layout build steps.
Keep them separate so context travels with the repo and mechanics travel with the skill.

## Placement
| Brand | Put this file | At |
|---|---|---|
| Tino Superapp | tino.CLAUDE.md | Tino repo root, renamed `CLAUDE.md` |
| Tino Go | tino-go.CLAUDE.md | Tino Go repo root |
| MMF | mmf.CLAUDE.md | MMF repo root |
| Midas | midas.CLAUDE.md | Midas repo root |
| CarMax | carmax.CLAUDE.md | CarMax repo root |

Fill every `TODO` once — that's the one-time cost that stops the repetition.
