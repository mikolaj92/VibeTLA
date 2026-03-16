#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
source_dir="$repo_root/.opencode/skills/feature-spec-planner"
target_dir="$HOME/.config/opencode/skill/feature-spec-planner"

mkdir -p "$(dirname "$target_dir")"
rm -rf "$target_dir"
ln -s "$source_dir" "$target_dir"
printf 'Installed OpenCode skill at %s\n' "$target_dir"
