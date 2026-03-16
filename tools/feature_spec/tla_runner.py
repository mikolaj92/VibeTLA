from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess


COMMON_JAR_LOCATIONS = [
    Path.home() / ".local" / "share" / "tla2tools.jar",
    Path.home() / "tla2tools.jar",
    Path("/opt/tla2tools.jar"),
    Path("/usr/local/share/tla2tools.jar"),
    Path("tla2tools.jar"),
]


@dataclass(slots=True)
class DoctorReport:
    python_ok: bool
    package_ok: bool
    java_ok: bool
    java_version: str | None
    java_path: str | None
    tla_jar_ok: bool
    tla_jar_path: str | None
    issues: list[str]


def find_tla_tools() -> Path | None:
    for env_name in ("TLATOOLS_JAR", "TLA2TOOLS_JAR"):
        value = os.getenv(env_name)
        if value:
            candidate = Path(value).expanduser()
            if candidate.exists():
                return candidate

    for candidate in COMMON_JAR_LOCATIONS:
        resolved = candidate.expanduser()
        if resolved.exists():
            return resolved
    return None


def java_version_info() -> tuple[bool, str | None, str | None]:
    java_path = shutil.which("java")
    if not java_path:
        return False, None, None
    result = subprocess.run([java_path, "-version"], capture_output=True, text=True, check=False)
    output = (result.stderr or result.stdout).splitlines()
    version_line = output[0] if output else None
    return True, version_line, java_path


def doctor_report() -> DoctorReport:
    issues: list[str] = []
    python_ok = True
    package_ok = True
    java_ok, version_line, java_path = java_version_info()
    if not java_ok:
        issues.append("java was not found on PATH; run `mise install`.")

    tla_jar = find_tla_tools()
    tla_jar_ok = tla_jar is not None
    if not tla_jar_ok:
        issues.append(
            "tla2tools.jar was not found; set TLATOOLS_JAR or place the jar in ~/.local/share/tla2tools.jar."
        )

    return DoctorReport(
        python_ok=python_ok,
        package_ok=package_ok,
        java_ok=java_ok,
        java_version=version_line,
        java_path=java_path,
        tla_jar_ok=tla_jar_ok,
        tla_jar_path=str(tla_jar) if tla_jar else None,
        issues=issues,
    )


def format_doctor_report(report: DoctorReport) -> str:
    lines = [
        f"python: {'ok' if report.python_ok else 'missing'}",
        f"package: {'ok' if report.package_ok else 'missing'}",
        f"java: {'ok' if report.java_ok else 'missing'}",
        f"java_path: {report.java_path or 'not found'}",
        f"java_version: {report.java_version or 'not found'}",
        f"tla2tools.jar: {'ok' if report.tla_jar_ok else 'missing'}",
        f"tla2tools.jar_path: {report.tla_jar_path or 'not found'}",
    ]
    if report.issues:
        lines.append("issues:")
        for issue in report.issues:
            lines.append(f"- {issue}")
    return "\n".join(lines)


def run_tlc(spec_dir: Path) -> subprocess.CompletedProcess[str]:
    spec_path = spec_dir / "spec.tla"
    model_path = spec_dir / "model.cfg"
    if not spec_path.exists():
        raise FileNotFoundError(f"Missing spec file: {spec_path}")
    if not model_path.exists():
        raise FileNotFoundError(f"Missing model config: {model_path}")

    report = doctor_report()
    if not report.java_ok or not report.tla_jar_ok or not report.tla_jar_path:
        raise RuntimeError(format_doctor_report(report))

    command = [
        report.java_path or "java",
        "-jar",
        report.tla_jar_path,
        "-cleanup",
        "-config",
        model_path.name,
        spec_path.name,
    ]
    return subprocess.run(command, cwd=spec_dir, capture_output=True, text=True, check=False)


def parse_tlc_output(result: subprocess.CompletedProcess[str]) -> tuple[bool, str]:
    output = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part).strip()
    if result.returncode == 0:
        return True, output or "TLC completed successfully."
    return False, output or f"TLC failed with exit code {result.returncode}."
