----------------------------- MODULE spec -----------------------------
EXTENDS TLC

\* Summary: Refresh session token with bounded retry and invalidation rules.
\* Assumption: only one refresh attempt is active per session
\* Assumption: retry is bounded by the caller before entering invalid
CONSTANTS States

VARIABLES state, previous_state

Init ==
  /\ state = "active"
  /\ previous_state = state

Beginrefresh ==
  /\ state \in { "active" }
  /\ previous_state' = state
  /\ state' = "refreshing"

Refreshsuccess ==
  /\ state \in { "refreshing" }
  /\ previous_state' = state
  /\ state' = "refreshed"

Refreshfailure ==
  /\ state \in { "refreshing" }
  /\ previous_state' = state
  /\ state' = "expired"

Invalidatesession ==
  /\ state \in { "active", "refreshed", "expired" }
  /\ previous_state' = state
  /\ state' = "invalid"

Stutter ==
  /\ state' = state
  /\ previous_state' = previous_state

Next ==
  Beginrefresh \/
  Refreshsuccess \/
  Refreshfailure \/
  Invalidatesession \/
  Stutter

TypeInvariant == state \in States /\ previous_state \in States
TransitionInvariant1 == ~(previous_state = "invalid" /\ state = "active")
Spec == Init /\ [][Next]_<<state, previous_state>>

=============================================================================
