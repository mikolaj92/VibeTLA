from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_opencode_skill.sh"
SKILL_SOURCE = REPO_ROOT / ".opencode" / "skills" / "feature-spec-planner"


def test_installer_defaults_to_opencode_skills_not_skill() -> None:
    text = INSTALLER.read_text()
    assert "$HOME/.config/opencode/skills" in text
    assert "$HOME/.config/opencode/skill/" not in text


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
