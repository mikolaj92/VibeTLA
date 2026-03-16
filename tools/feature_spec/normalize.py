from __future__ import annotations

from pathlib import Path
import re

from pydantic import BaseModel, Field

from .parser import ParsedTask


class Transition(BaseModel):
    name: str
    from_states: list[str] = Field(default_factory=list)
    to_state: str


class FeatureModel(BaseModel):
    task_id: str
    summary: str
    entities: list[str] = Field(default_factory=list)
    states: list[str] = Field(default_factory=list)
    transitions: list[Transition] = Field(default_factory=list)
    invariants: list[str] = Field(default_factory=list)
    forbidden_states: list[str] = Field(default_factory=list)
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


def normalize_feature(parsed: ParsedTask, task_id: str | None = None) -> FeatureModel:
    raw_summary = " ".join(parsed.sections.get("summary", [])).strip() or parsed.title or "Untitled feature"
    resolved_task_id = extract_task_id(parsed.source, raw_summary, explicit=task_id)

    transitions: list[Transition] = []
    for item in parsed.sections.get("transitions", []):
        transition = parse_transition(item)
        if transition:
            transitions.append(transition)

    states: list[str] = [slugify(state) for state in parsed.sections.get("states", []) if state.strip()]
    if not states:
        inferred_states: list[str] = []
        for transition in transitions:
            inferred_states.extend(transition.from_states)
            inferred_states.append(transition.to_state)
        states = list(dict.fromkeys(inferred_states))
    if not states:
        states = ["draft"]

    entities = [slugify(item) for item in parsed.sections.get("entities", []) if item.strip()]
    summary = raw_summary[0].upper() + raw_summary[1:] if raw_summary else "Untitled feature"

    return FeatureModel(
        task_id=resolved_task_id,
        summary=summary,
        entities=entities,
        states=list(dict.fromkeys(states)),
        transitions=transitions,
        invariants=parsed.sections.get("invariants", []),
        forbidden_states=parsed.sections.get("forbidden_states", []),
        assumptions=parsed.sections.get("assumptions", []),
        non_goals=parsed.sections.get("non_goals", []),
        source=parsed.source,
    )
