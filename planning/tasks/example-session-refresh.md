# Summary

Refresh session token with bounded retry and invalidation rules.

## Entities

- session
- refresh_token
- access_token

## States

- active
- refreshing
- refreshed
- expired
- invalid

## Transitions

- begin_refresh: active -> refreshing
- refresh_success: refreshing -> refreshed
- refresh_failure: refreshing -> expired
- invalidate_session: active, refreshed, expired -> invalid

## Invariants

- transition != invalid -> active

## Forbidden states



## Assumptions

- only one refresh attempt is active per session
- retry is bounded by the caller before entering invalid

## Non-goals

- UI for login prompts
