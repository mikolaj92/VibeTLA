from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .bundle import write_bundle
from .normalize import FeatureModel


TEMPLATE_ROOT = Path(__file__).parent / "templates"


def template_environment() -> Environment:
    return Environment(loader=FileSystemLoader(str(TEMPLATE_ROOT)), trim_blocks=True, lstrip_blocks=True)


def render_template(template_name: str, context: Mapping[str, object]) -> str:
    return template_environment().get_template(template_name).render(**context).strip() + "\n"


def ensure_empty_spec_dir(spec_dir: Path) -> None:
    if spec_dir.exists() and any(spec_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite existing spec directory: {spec_dir}")
    spec_dir.mkdir(parents=True, exist_ok=True)


def write_spec_pack(spec_dir: Path, model: FeatureModel) -> list[Path]:
    ensure_empty_spec_dir(spec_dir)
    context = {"model": model}
    outputs = {
        spec_dir / "plan.md": render_template("plan.md.j2", context),
        spec_dir / "spec.tla": render_template("spec.tla.j2", context),
        spec_dir / "model.cfg": render_template("model.cfg.j2", context),
        spec_dir / "impl.md": render_template("impl.md.j2", context),
        spec_dir / "tests.md": render_template("tests.md.j2", context),
    }
    written_paths: list[Path] = []
    for path, content in outputs.items():
        _ = path.write_text(content, encoding="utf-8")
        written_paths.append(path)
    written_paths.append(write_bundle(spec_dir, model))
    return written_paths
