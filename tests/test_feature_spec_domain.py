import json
from pathlib import Path

import pytest
from feature_spec.bundle import build_bundle_payload
from feature_spec.cli import app
from feature_spec.normalize import normalize_feature
from feature_spec.parser import parse_task_text
from feature_spec.planner import plan_feature
from feature_spec.tla_runner import doctor_report, run_tlc
from typer.testing import CliRunner

STRUCTURED = """# Demo
## States
- idle
- ready
- forbidden
## Transitions
- activate: idle -> ready
## Invariants
- transition != ready -> idle
## Forbidden states
- state != forbidden
"""


def test_parser_and_normalizer_keep_domain_sections() -> None:
    parsed = parse_task_text(STRUCTURED)
    assert parsed.sections["states"] == ["idle", "ready", "forbidden"]
    assert parsed.sections["transitions"] == ["activate: idle -> ready"]
    model = normalize_feature(parsed, task_id="demo")
    assert model.task_id == "demo"
    assert model.transitions[0].from_states == ["idle"]
    assert model.state_invariants[0].forbidden_state == "forbidden"
    assert model.transition_invariants[0].to_state == "idle"


@pytest.mark.parametrize("text, missing", [
    ("loose prose", "## States and ## Transitions"),
    ("## States\n- idle", "## Transitions"),
    ("## Transitions\n- go: idle -> ready", "## States"),
])
def test_unstructured_input_fails_closed_without_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, text: str, missing: str) -> None:
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["plan", "--from-text", text, "--task-id", "draft"])
    assert result.exit_code != 0
    assert missing in result.output
    assert not (tmp_path / "specs" / "draft").exists()


def test_plan_refuses_overwrite_and_bundle_has_paths(tmp_path: Path) -> None:
    task = tmp_path / "new-flow.md"
    task.write_text(STRUCTURED)
    model, spec_dir, written = plan_feature(path=task, output_root=tmp_path / "specs")
    assert {path.name for path in written} == {"plan.md", "spec.tla", "model.cfg", "impl.md", "tests.md", "bundle.json"}
    payload = json.loads((spec_dir / "bundle.json").read_text())
    assert payload["task_id"] == model.task_id == "new-flow"
    assert payload["transitions"][0] == {"name": "activate", "from": ["idle"], "to": "ready"}
    assert payload["paths"]["spec"].endswith("spec.tla")
    with pytest.raises(FileExistsError):
        plan_feature(path=task, output_root=tmp_path / "specs")


def test_bundle_payload_is_json_serializable(tmp_path: Path) -> None:
    model = normalize_feature(parse_task_text(STRUCTURED), task_id="demo")
    json.dumps(build_bundle_payload(model, tmp_path / "demo"))


def test_check_reports_missing_spec(tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["check", str(tmp_path)])
    assert result.exit_code != 0
    assert "Missing spec file" in result.output


def test_tlc_checks_generated_invariants(tmp_path: Path) -> None:
    report = doctor_report()
    if not report.java_ok or not report.tla_jar_ok:
        pytest.skip("TLC is genuinely unavailable")
    task = tmp_path / "unsafe.md"
    task.write_text("""## States
- invalid
- active
## Transitions
- reactivate: invalid -> active
## Invariants
- transition != invalid -> active
""")
    _, spec_dir, _ = plan_feature(path=task, output_root=tmp_path / "specs")
    result = run_tlc(spec_dir)
    assert result.returncode != 0
    assert "Invariant TransitionInvariant1 is violated" in result.stdout


def test_check_succeeds_for_checked_example() -> None:
    report = doctor_report()
    if not report.java_ok or not report.tla_jar_ok:
        pytest.skip("TLC is genuinely unavailable")
    root = Path(__file__).resolve().parents[1]
    result = run_tlc(root / "specs" / "example-session-refresh")
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_writes_to_explicit_target_repo(tmp_path: Path) -> None:
    task = tmp_path / "task.md"
    task.write_text(STRUCTURED)
    output_root = tmp_path / "target" / "specs"
    result = CliRunner().invoke(app, ["plan", str(task), "--output-root", str(output_root)])
    assert result.exit_code == 0, result.output
    assert (output_root / "task" / "spec.tla").exists()


def test_generated_plan_round_trips_through_bundle(tmp_path: Path) -> None:
    task = tmp_path / "roundtrip.md"
    task.write_text(STRUCTURED)
    _, spec_dir, _ = plan_feature(path=task, output_root=tmp_path / "specs")
    result = CliRunner().invoke(app, ["bundle", str(spec_dir)])
    assert result.exit_code == 0, result.output
