from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = [
    ROOT / ".opencode/skills/feature-spec-planner/SKILL.md",
    ROOT / "codex/skill/feature-spec-planner/SKILL.md",
]


def test_skill_copies_are_identical_and_have_frontmatter() -> None:
    texts = [path.read_text() for path in SKILLS]
    assert texts[0] == texts[1]
    assert texts[0].startswith("---\n")
    _, frontmatter, _ = texts[0].split("---", 2)
    assert "name: feature-spec-planner" in frontmatter
    assert "description:" in frontmatter
    assert "TLA+" in frontmatter
    assert "uv run feature-spec plan" in texts[0]
    assert "Do not write or edit `spec.tla` manually" in texts[0]
