# Required behavior

- Implement the states and transitions defined in `plan.md`.
- Preserve the checked transition graph from `spec.tla`.

## Constraints

- keep the runtime behavior aligned with the spec pack

## Persistence expectations

- persist enough state to enforce the transition model

## Do not do

- do not add extra product scope outside the pack

## Suggested implementation order

1. Add the state model.
2. Implement the named transitions.
3. Enforce invariant-related constraints.
4. Add tests from `tests.md`.
