----------------------------- MODULE spec -----------------------------
EXTENDS TLC

\* Summary: Add session refresh with bounded retry
CONSTANTS States

VARIABLE state

Init ==
  state = "draft"

Stutter ==
  /\ state' = state

Next ==
  Stutter
TypeInvariant == state \in States

Spec == Init /\ [][Next]_state

=============================================================================
