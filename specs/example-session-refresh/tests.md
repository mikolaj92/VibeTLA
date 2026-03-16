# Happy paths

- begin-refresh moves active to refreshing
- refresh-success moves refreshing to refreshed
- refresh-failure moves refreshing to expired
- invalidate-session moves active, refreshed, expired to invalid

## Invalid transitions

- reject transitions that are not enabled from `active`
- reject transitions that are not enabled from `refreshing`
- reject transitions that are not enabled from `refreshed`
- reject transitions that are not enabled from `expired`
- reject transitions that are not enabled from `invalid`

## Invariant checks

- invalid sessions cannot become active again
- a session cannot be both expired and refreshed

## Failure cases

- ensure the system never reaches: session is both active and expired

## Retry/idempotency

- verify: only one refresh attempt is active per session
- verify: retry is bounded by the caller before entering invalid

## Property-based ideas

- generate transition sequences and assert all reachable states stay within the declared graph
