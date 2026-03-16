from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .bundle import load_model_from_plan, write_bundle
from .planner import plan_feature
from .tla_runner import doctor_report, format_doctor_report, parse_tlc_output, run_tlc


app = typer.Typer(help="Plan features before coding with formal specs and TLA+ checks.")


@app.command()
def plan(
    path: Annotated[str, typer.Argument(help="Path to a task markdown file.")] = "",
    from_text: Annotated[str, typer.Option("--from-text", help="Plan directly from raw text.")] = "",
    task_id: Annotated[str, typer.Option("--task-id", help="Override the derived task id.")] = "",
) -> None:
    """Create a spec pack from a task file or raw text."""

    resolved_path = Path(path) if path else None
    try:
        model, spec_dir, written = plan_feature(
            path=resolved_path,
            from_text=from_text or None,
            task_id=task_id or None,
        )
    except (FileNotFoundError, FileExistsError, ValueError) as error:
        raise typer.Exit(code=_fail(str(error))) from error

    typer.echo(f"planned: {model.task_id}")
    typer.echo(f"spec_dir: {spec_dir}")
    for written_path in written:
        typer.echo(f"wrote: {written_path}")


@app.command()
def check(spec_dir: str) -> None:
    """Run TLC against a generated spec pack."""

    try:
        result = run_tlc(Path(spec_dir))
    except (FileNotFoundError, RuntimeError) as error:
        raise typer.Exit(code=_fail(str(error))) from error

    ok, output = parse_tlc_output(result)
    typer.echo(output)
    if not ok:
        raise typer.Exit(code=1)


@app.command()
def bundle(spec_dir: str) -> None:
    """Rebuild bundle.json for a generated spec pack."""

    resolved_dir = Path(spec_dir)
    missing = [
        path.name
        for path in [
            resolved_dir / "plan.md",
            resolved_dir / "spec.tla",
            resolved_dir / "model.cfg",
            resolved_dir / "impl.md",
            resolved_dir / "tests.md",
        ]
        if not path.exists()
    ]
    if missing:
        raise typer.Exit(code=_fail(f"Missing required artifact(s): {', '.join(missing)}"))

    model = load_model_from_plan(resolved_dir)
    bundle_path = write_bundle(resolved_dir, model)
    typer.echo(f"wrote: {bundle_path}")


@app.command()
def doctor() -> None:
    """Check whether the local environment can run TLC."""

    report = doctor_report()
    typer.echo(format_doctor_report(report))
    if report.issues:
        raise typer.Exit(code=1)


def _fail(message: str) -> int:
    _ = typer.secho(message, fg=typer.colors.RED, err=True)
    return 1


if __name__ == "__main__":
    app()
