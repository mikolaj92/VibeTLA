from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_opencode_skill.sh"
SKILL_SOURCE = REPO_ROOT / ".opencode" / "skills" / "feature-spec-planner"


def test_installer_defaults_to_opencode_skills_not_skill() -> None:
    text = INSTALLER.read_text()
    assert 'base_dir="${OPENCODE_SKILL_DIR:-$HOME/.config/opencode/skills}"' in text
    assert 'target_dir="$base_dir/feature-spec-planner"' in text


def test_installer_links_skill_into_opencode_skills_dir(tmp_path: Path) -> None:
    home = tmp_path / "home"
    result = subprocess.run(
        [str(INSTALLER)],
        check=True,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "HOME": str(home),
        },
    )

    target = home / ".config" / "opencode" / "skills" / "feature-spec-planner"
    assert target.is_symlink()
    assert target.resolve() == SKILL_SOURCE.resolve()
    assert str(target) in result.stdout
    assert not (home / ".config" / "opencode" / "skill").exists()


def test_installer_honors_override(tmp_path: Path) -> None:
    destination = tmp_path / "custom-skills"
    subprocess.run(
        [str(INSTALLER)],
        check=True,
        env={**os.environ, "HOME": str(tmp_path / "home"), "OPENCODE_SKILL_DIR": str(destination)},
    )
    assert (destination / "feature-spec-planner").resolve() == SKILL_SOURCE.resolve()


def test_default_installer_removes_singular_leftover(tmp_path: Path) -> None:
    home = tmp_path / "home"
    leftover = home / ".config" / "opencode" / "skill" / "feature-spec-planner"
    leftover.mkdir(parents=True)
    (leftover / "stale").write_text("stale")
    subprocess.run([str(INSTALLER)], check=True, env={**os.environ, "HOME": str(home)})
    assert not leftover.exists()
