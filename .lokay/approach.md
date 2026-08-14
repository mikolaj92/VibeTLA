# Approach plan

<!-- lokay-approach source=deterministic repo=mikolaj92/VibeTLA issue=14 -->

Repository: `mikolaj92/VibeTLA`  
Issue: #14 — Installer Codex skill ląduje w ~/.config/codex/skill zamiast ~/.codex/skills

## Goal

`scripts/install_codex_skill.sh` + README: `~/.config/codex/skill/feature-spec-planner`.
Codex CLI (i sibling VibeFront `install_codex_skill.sh`) używa `~/.codex/skills`.

## Files likely touched

- `scripts/install_codex_skill.sh`
- `install_codex_skill.sh`

## Test plan

- Run the smallest useful tests for files touched

## Non-goals

- (none stated)

## Notes

- Trust intentional issue; this plan is evidence for later review, not a human gate.
- Coding agent may refine details but should stay on the stated goal and non-goals.
- Collector boundary: if implementation introduces unbounded collection, ship only a bounded collector patch that starts durably in the background after merge. The coding agent and mill must not populate data or wait for collection to finish.
