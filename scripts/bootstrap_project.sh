#!/usr/bin/env bash
set -euo pipefail

target_dir="${1:-$PWD}"

mkdir -p "$target_dir"
target_dir="$(cd "$target_dir" && pwd)"

mkdir -p "$target_dir/planning/tasks"
mkdir -p "$target_dir/specs"

gitignore_path="$target_dir/.gitignore"
touch "$gitignore_path"

ensure_gitignore_line() {
  local line="$1"
  if ! grep -Fqx "$line" "$gitignore_path"; then
    printf '%s\n' "$line" >> "$gitignore_path"
  fi
}

ensure_gitignore_line "# VibeTLA"
ensure_gitignore_line "states/"

printf 'Bootstrapped VibeTLA project directories in %s\n' "$target_dir"
printf 'Created: %s\n' "$target_dir/planning/tasks"
printf 'Created: %s\n' "$target_dir/specs"
printf 'Updated: %s\n' "$gitignore_path"
