#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
source_dir="$repo_root/codex/skill/feature-spec-planner"
base_dir="${CODEX_SKILL_DIR:-$HOME/.codex/skills}"
target_dir="$base_dir/feature-spec-planner"

mkdir -p "$base_dir"
rm -rf "$target_dir"
ln -s "$source_dir" "$target_dir"
printf 'Installed Codex skill at %s\n' "$target_dir"
