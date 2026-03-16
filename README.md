# VibeTLA

Spec-first planning toolkit for Codex and OpenCode.

VibeTLA turns a textual feature description into:
- a formal TLA+ spec
- a checked planning pack
- implementation guidance
- testing guidance
- a machine-readable bundle for an implementation agent

The core rule is simple: no code before spec for non-trivial features.

## Why

Use VibeTLA before coding stateful or risky work. The planner layer writes the model first, checks it with TLC, and only then hands work to the coding agent.

## Workflow

1. Put a task in `planning/tasks/` or pass text directly.
2. Run `mise install` once for local tooling.
3. Run `uv run feature-spec plan ...`.
4. Run `uv run feature-spec check ...`.
5. Run `uv run feature-spec bundle ...`.
6. Hand the checked bundle to the implementation agent.

## Commands

```bash
mise install
uv run feature-spec plan planning/tasks/example-session-refresh.md
uv run feature-spec check specs/example-session-refresh
uv run feature-spec bundle specs/example-session-refresh
uv run feature-spec doctor
uv run feature-spec plan --from-text "Add session refresh with bounded retry"
```

## Folder Structure

- `.opencode/skills/feature-spec-planner/` - OpenCode skill assets
- `codex/skill/feature-spec-planner/` - Codex skill assets
- `tools/feature_spec/` - CLI package and templates
- `planning/tasks/` - raw feature inputs
- `specs/` - generated formal and implementation artifacts
- `docs/` - project documentation
- `scripts/` - local install and environment helpers

## Tooling

This repo uses `mise` to pin Python, Java, and `uv`, and uses `uv` to run the CLI.

## Skill Installation

```bash
./scripts/install_opencode_skill.sh
./scripts/install_codex_skill.sh
```
