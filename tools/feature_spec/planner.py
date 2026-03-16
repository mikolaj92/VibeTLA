from __future__ import annotations

from pathlib import Path

from .normalize import FeatureModel, normalize_feature
from .parser import parse_task_text, read_task_file
from .writer import write_spec_pack


def build_feature_model(path: Path | None = None, from_text: str | None = None, task_id: str | None = None) -> FeatureModel:
    if path is None and not from_text:
        raise ValueError("Provide a task file path or --from-text.")
    if path is not None and from_text:
        raise ValueError("Use either a task file path or --from-text, not both.")

    if path is not None:
        parsed = read_task_file(path)
    else:
        parsed = parse_task_text(from_text or "", source="<text>", title_hint=task_id)

    return normalize_feature(parsed, task_id=task_id)


def plan_feature(path: Path | None = None, from_text: str | None = None, output_root: Path | None = None, task_id: str | None = None) -> tuple[FeatureModel, Path, list[Path]]:
    model = build_feature_model(path=path, from_text=from_text, task_id=task_id)
    resolved_root = output_root or Path("specs")
    spec_dir = resolved_root / model.task_id
    written = write_spec_pack(spec_dir, model)
    return model, spec_dir, written
