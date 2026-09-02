from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, Field

from .parser import ParsedTask


class Transition(BaseModel):
    name: str
    from_states: list[str] = Field(default_factory=list)
    to_state: str


class StateInvariant(BaseModel):
    name: str
    forbidden_state: str


class TransitionInvariant(BaseModel):
    name: str
    from_state: str
    to_state: str


class FeatureModel(BaseModel):
    task_id: str
    summary: str
    entities: list[str] = Field(default_factory=list)
    states: list[str] = Field(default_factory=list)
    transitions: list[Transition] = Field(default_factory=list)
    invariants: list[str] = Field(default_factory=list)
    forbidden_states: list[str] = Field(default_factory=list)
    state_invariants: list[StateInvariant] = Field(default_factory=list)
    transition_invariants: list[TransitionInvariant] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    source: str


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    dashed = re.sub(r"[^a-z0-9]+", "-", lowered)
    return dashed.strip("-") or "feature-spec"


def extract_task_id(source_name: str | None, summary: str, explicit: str | None = None) -> str:
    if explicit:
        return slugify(explicit)
    if source_name:
        stem = Path(source_name).stem
        if stem and stem != "<text>":
            return slugify(stem)
    return slugify(summary)


def parse_transition(line: str) -> Transition | None:
    match = re.match(r"^(?P<name>[a-zA-Z0-9_-]+)\s*:\s*(?P<from>.+?)\s*->\s*(?P<to>[a-zA-Z0-9_-]+)$", line)
    if not match:
        return None
    from_states = [slugify(part) for part in match.group("from").split(",") if part.strip()]
    return Transition(
        name=slugify(match.group("name")),
        from_states=from_states,
        to_state=slugify(match.group("to")),
    )


def _invariant_name(prefix: str, index: int) -> str:
    return f"{prefix}{index + 1}"


def parse_state_invariant(line: str, index: int) -> StateInvariant:
    match = re.fullmatch(r"state != ([a-zA-Z0-9_-]+)", line.strip())
    if not match:
        raise ValueError(
            "Unsupported invariant. Use the explicit syntax `state != <state>` "
            "or `transition != <from> -> <to>`."
        )
    return StateInvariant(name=_invariant_name("StateInvariant", index), forbidden_state=slugify(match.group(1)))


def parse_transition_invariant(line: str, index: int) -> TransitionInvariant:
    match = re.fullmatch(r"transition != ([a-zA-Z0-9_-]+)\s*->\s*([a-zA-Z0-9_-]+)", line.strip())
    if not match:
        raise ValueError(
            "Unsupported invariant. Use the explicit syntax `state != <state>` "
            "or `transition != <from> -> <to>`."
        )
    return TransitionInvariant(
        name=_invariant_name("TransitionInvariant", index),
        from_state=slugify(match.group(1)),
        to_state=slugify(match.group(2)),
    )


def normalize_feature(parsed: ParsedTask, task_id: str | None = None) -> FeatureModel:
    raw_summary = " ".join(parsed.sections.get("summary", [])).strip() or parsed.title or "Untitled feature"
    resolved_task_id = extract_task_id(parsed.source, raw_summary, explicit=task_id)

    raw_states = [item for item in parsed.sections.get("states", []) if item.strip()]
    raw_transitions = [item for item in parsed.sections.get("transitions", []) if item.strip()]
    if not raw_states or not raw_transitions:
        missing = []
        if not raw_states:
            missing.append("## States")
        if not raw_transitions:
            missing.append("## Transitions")
        raise ValueError(f"Task must define non-empty {' and '.join(missing)} sections.")

    transitions: list[Transition] = []
    for item in raw_transitions:
        transition = parse_transition(item)
        if transition is None:
            raise ValueError(f"Invalid transition `{item}`; expected `name: from -> to`.")
        transitions.append(transition)

    states = list(dict.fromkeys(slugify(state) for state in raw_states))
    defined_states = set(states)
    referenced_states = {
        state
        for transition in transitions
        for state in [*transition.from_states, transition.to_state]
    }
    undefined_states = referenced_states - defined_states
    if undefined_states:
        raise ValueError(f"Transitions reference undefined states: {sorted(undefined_states)}.")

    raw_invariants = parsed.sections.get("invariants", [])
    state_invariants: list[StateInvariant] = []
    transition_invariants: list[TransitionInvariant] = []
    for item in raw_invariants:
        if item.strip().startswith("state !="):
            state_invariants.append(parse_state_invariant(item, len(state_invariants)))
        elif item.strip().startswith("transition !="):
            transition_invariants.append(parse_transition_invariant(item, len(transition_invariants)))
        else:
            raise ValueError(
                f"Unsupported invariant `{item}`. Use `state != <state>` or `transition != <from> -> <to>`."
            )

    raw_forbidden = [
        item for item in parsed.sections.get("forbidden_states", []) if item != "none specified"
    ]
    for item in raw_forbidden:
        state_invariants.append(parse_state_invariant(item, len(state_invariants)))

    for invariant in state_invariants:
        if invariant.forbidden_state not in defined_states:
            raise ValueError(f"Invariant references undefined state: {invariant.forbidden_state}.")
    for invariant in transition_invariants:
        if invariant.from_state not in defined_states or invariant.to_state not in defined_states:
            raise ValueError(
                f"Invariant references undefined transition states: {invariant.from_state} -> {invariant.to_state}."
            )

    entities = [slugify(item) for item in parsed.sections.get("entities", []) if item.strip()]
    summary = raw_summary[0].upper() + raw_summary[1:] if raw_summary else "Untitled feature"
    return FeatureModel(
        task_id=resolved_task_id,
        summary=summary,
        entities=entities,
        states=states,
        transitions=transitions,
        invariants=raw_invariants,
        forbidden_states=raw_forbidden,
        state_invariants=state_invariants,
        transition_invariants=transition_invariants,
        assumptions=parsed.sections.get("assumptions", []),
        non_goals=parsed.sections.get("non_goals", []),
        source=parsed.source,
    )
