#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
source_dir="$repo_root/.opencode/skills/feature-spec-planner"
base_dir="${OPENCODE_SKILL_DIR:-$HOME/.config/opencode/skills}"
target_dir="$base_dir/feature-spec-planner"

if [[ -z "${OPENCODE_SKILL_DIR:-}" ]]; then
    rm -rf "$HOME/.config/opencode/skill/feature-spec-planner"
fi
mkdir -p "$base_dir"
rm -rf "$target_dir"
ln -s "$source_dir" "$target_dir"
printf 'Installed OpenCode skill at %s
' "$target_dir"
