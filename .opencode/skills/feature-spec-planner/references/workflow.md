# workflow

1. Read the feature description.
2. Identify entities, states, transitions, invariants, assumptions, and non-goals.
3. Produce `plan.md`.
4. Produce `spec.tla` and `model.cfg`.
5. Validate the model.
6. Produce `impl.md`, `tests.md`, and `bundle.json`.
7. Hand off the checked bundle to the implementation agent.

Never skip the modeling step for stateful or non-trivial work.
Never paper over ambiguity with fallback behavior.
