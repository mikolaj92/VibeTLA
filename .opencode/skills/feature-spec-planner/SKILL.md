---
name: feature-spec-planner
description: Plan stateful features with the VibeTLA CLI, TLA+, and TLC before implementation. Use for risky workflows that need explicit states, transitions, and checked invariants.
---

# Feature Spec Planner

Use the VibeTLA checkout at `~/.local/share/vibetla` or another stable clone as the CLI working directory. Keep task inputs and generated `planning/tasks/` and `specs/` artifacts in the target repository by passing their paths explicitly.

Run the product pipeline instead of writing TLA+ by hand:

1. Create a structured task file with non-empty `## States` and `## Transitions`, or pass the same structured Markdown through `--from-text`.
2. From the VibeTLA checkout, run `uv run feature-spec plan <target-task-path> --output-root <target-repo>/specs`.
3. Run `uv run feature-spec check <target-spec-directory>`.
4. Run `uv run feature-spec bundle <target-spec-directory>`.
5. Hand off the checked `bundle.json` to the implementation agent.

Rules:

- No code before a checked spec for non-trivial stateful features.
- Do not write or edit `spec.tla` manually. The CLI is the only generator.
- Do not invent a manual fallback when the CLI is unavailable. Run `uv run feature-spec doctor` and stop on failure.
- Do not paper over ambiguity with fallback behavior.
- Keep the model small and explicit.
- Keep implementation and test guidance aligned with the checked pack.
