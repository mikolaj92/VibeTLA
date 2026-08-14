from __future__ import annotations

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_codex_skill.sh"
SKILL_SOURCE = REPO_ROOT / "codex" / "skill" / "feature-spec-planner"


def test_installer_defaults_to_codex_skills_not_config_skill() -> None:
    text = INSTALLER.read_text()
    assert "$HOME/.codex/skills" in text
    assert "$HOME/.config/codex/skill" not in text


def test_installer_links_skill_into_codex_skills_dir(tmp_path: Path) -> None:
    dest = tmp_path / "skills"
    result = subprocess.run(
        [str(INSTALLER)],
        check=True,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "CODEX_SKILL_DIR": str(dest),
            "HOME": str(tmp_path / "home"),
        },
    )

    target = dest / "feature-spec-planner"
    assert target.is_symlink()
    assert target.resolve() == SKILL_SOURCE.resolve()
    assert str(target) in result.stdout
    assert not (tmp_path / "home" / ".config" / "codex" / "skill").exists()
