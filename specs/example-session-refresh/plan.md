# Summary

Refresh session token with bounded retry and invalidation rules.

## Entities

- session
- refresh-token
- access-token

## States

- active
- refreshing
- refreshed
- expired
- invalid

## Transitions

- begin-refresh: active -> refreshing
- refresh-success: refreshing -> refreshed
- refresh-failure: refreshing -> expired
- invalidate-session: active, refreshed, expired -> invalid

## Invariants

- transition != invalid -> active

## Forbidden states

- none specified

## Assumptions

- only one refresh attempt is active per session
- retry is bounded by the caller before entering invalid

## Non-goals

- UI for login prompts
