----------------------------- MODULE spec -----------------------------
EXTENDS TLC

\* Summary: Refresh session token with bounded retry and invalidation rules.
\* Invariant note: invalid sessions cannot become active again
\* Invariant note: a session cannot be both expired and refreshed
\* Assumption: only one refresh attempt is active per session
\* Assumption: retry is bounded by the caller before entering invalid
CONSTANTS States

VARIABLE state

Init ==
  state = "active"

Beginrefresh ==
  /\ state \in { "active" }
  /\ state' = "refreshing"

Refreshsuccess ==
  /\ state \in { "refreshing" }
  /\ state' = "refreshed"

Refreshfailure ==
  /\ state \in { "refreshing" }
  /\ state' = "expired"

Invalidatesession ==
  /\ state \in { "active", "refreshed", "expired" }
  /\ state' = "invalid"

Stutter ==
  /\ state' = state

Next ==
  Beginrefresh \/
  Refreshsuccess \/
  Refreshfailure \/
  Invalidatesession \/
  Stutter
TypeInvariant == state \in States

Spec == Init /\ [][Next]_state

=============================================================================
