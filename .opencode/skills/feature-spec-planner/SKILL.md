# Feature Spec Planner

Use this skill when you need to plan a non-trivial feature before coding.

The workflow is:

1. Read the feature description.
2. Identify entities, states, transitions, invariants, assumptions, and non-goals.
3. Produce `plan.md`.
4. Produce `spec.tla` and `model.cfg`.
5. Validate the model with TLC.
6. Produce `impl.md`, `tests.md`, and `bundle.json`.
7. Hand off the checked bundle to the implementation agent.

Rules:

- No code before spec for non-trivial features.
- Do not skip the modeling step for stateful workflows.
- Do not paper over ambiguity with fallback behavior.
- Keep the model small and explicit.
- Keep implementation and test guidance aligned with the checked pack.
