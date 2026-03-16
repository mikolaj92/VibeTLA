from __future__ import annotations

import json
from pathlib import Path

from .normalize import FeatureModel, normalize_feature
from .parser import parse_task_text


def build_bundle_payload(model: FeatureModel, spec_dir: Path) -> dict[str, object]:
    return {
        "task_id": model.task_id,
        "summary": model.summary,
        "entities": model.entities,
        "states": model.states,
        "transitions": [
            {
                "name": transition.name,
                "from": transition.from_states,
                "to": transition.to_state,
            }
            for transition in model.transitions
        ],
        "invariants": model.invariants,
        "forbidden_states": model.forbidden_states,
        "assumptions": model.assumptions,
        "non_goals": model.non_goals,
        "paths": {
            "plan": str(spec_dir / "plan.md"),
            "spec": str(spec_dir / "spec.tla"),
            "model": str(spec_dir / "model.cfg"),
            "impl": str(spec_dir / "impl.md"),
            "tests": str(spec_dir / "tests.md"),
            "bundle": str(spec_dir / "bundle.json"),
        },
        "implementation_warnings": [
            "Do not introduce fallback behavior that violates the checked model.",
            "Keep runtime transitions aligned with the named states and transitions in the pack.",
        ],
        "testing_obligations": [
            "Cover happy paths for each named transition.",
            "Verify illegal transitions are rejected.",
            "Assert invariants are preserved across retries and failures.",
        ],
    }


def load_model_from_plan(spec_dir: Path) -> FeatureModel:
    plan_path = spec_dir / "plan.md"
    parsed = parse_task_text(plan_path.read_text(encoding="utf-8"), source=str(plan_path), title_hint=spec_dir.name)
    return normalize_feature(parsed, task_id=spec_dir.name)


def write_bundle(spec_dir: Path, model: FeatureModel) -> Path:
    bundle_path = spec_dir / "bundle.json"
    payload = build_bundle_payload(model, spec_dir)
    bundle_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return bundle_path
