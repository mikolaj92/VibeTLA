# Happy paths

- cover the baseline state initialization path

## Invalid transitions

- reject transitions that are not enabled from `draft`

## Invariant checks

- assert runtime state always remains within the declared states set

## Failure cases

- verify invalid or conflicting state updates are rejected

## Retry/idempotency

- verify repeated calls do not violate the state machine

## Property-based ideas

- generate transition sequences and assert all reachable states stay within the declared graph
