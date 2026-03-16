# Required behavior

- Implement the states and transitions defined in `plan.md`.
- Preserve the checked transition graph from `spec.tla`.

## Constraints

- invalid sessions cannot become active again
- a session cannot be both expired and refreshed

## Persistence expectations

- only one refresh attempt is active per session
- retry is bounded by the caller before entering invalid

## Do not do

- UI for login prompts

## Suggested implementation order

1. Add the state model.
2. Implement the named transitions.
3. Enforce invariant-related constraints.
4. Add tests from `tests.md`.
