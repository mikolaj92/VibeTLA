# VibeTLA

Spec-first planning toolkit for Codex and OpenCode.

VibeTLA turns a textual feature description into:
- a formal TLA+ spec
- a checked planning pack
- implementation guidance
- testing guidance
- a machine-readable bundle for an implementation agent

The core rule is simple: no code before spec for non-trivial features.

## Why

Use VibeTLA before coding stateful or risky work. The planner layer writes the model first, checks it with TLC, and only then hands work to the coding agent.

## Workflow

1. Put a task in `planning/tasks/` or pass text directly.
2. Run `mise install` once for local tooling.
3. Run `uv run feature-spec plan ...`.
4. Run `uv run feature-spec check ...`.
5. Run `uv run feature-spec bundle ...`.
6. Hand the checked bundle to the implementation agent.

## Commands

```bash
mise install
uv run feature-spec plan planning/tasks/example-session-refresh.md
uv run feature-spec check specs/example-session-refresh
uv run feature-spec bundle specs/example-session-refresh
uv run feature-spec doctor
uv run feature-spec plan --from-text "Add session refresh with bounded retry"
```

## Folder Structure

- `.opencode/skills/feature-spec-planner/` - OpenCode skill assets
- `codex/skill/feature-spec-planner/` - Codex skill assets
- `tools/feature_spec/` - CLI package and templates
- `planning/tasks/` - raw feature inputs
- `specs/` - generated formal and implementation artifacts
- `docs/` - project documentation
- `scripts/` - local install and environment helpers

## Tooling

This repo uses `mise` to pin Python, Java, and `uv`, and uses `uv` to run the CLI.

## Skill Installation

Use the curl installer if you want the shortest path for an agent or a fresh machine:

```bash
curl -fsSL https://raw.githubusercontent.com/mikolaj92/VibeTLA/main/install.sh | bash
```

This installer:

- clones or updates VibeTLA in `~/.local/share/vibetla`
- installs the OpenCode skill link
- installs the Codex skill link

It does not install into `/tmp` or `/private/...`.

If you already have the repo locally, you can still run the lower-level scripts directly:

```bash
./scripts/install_opencode_skill.sh
./scripts/install_codex_skill.sh
```

These scripts install the skill globally for the current user by creating symlinks in:

- `~/.config/opencode/skill/feature-spec-planner`
- `~/.config/codex/skill/feature-spec-planner`

The skill definition stays in a stable local repository checkout and the global config points to it.

## Project Bootstrap

If you want to prepare a target repository for VibeTLA artifacts, use the in-repo bootstrap script:

```bash
./scripts/bootstrap_project.sh /path/to/project
```

If you run it inside an existing project repository, you can also call it without arguments:

```bash
./scripts/bootstrap_project.sh
```

The bootstrap script only prepares project-local state:

- `planning/tasks/`
- `specs/`
- `.gitignore` entry for `states/`

It does not install the skill globally. Use the install scripts for that.

## Installation Model

VibeTLA uses a two-part installation model.

### 1. Global skill installation

Install the skill once per machine through `install.sh` or the scripts in `scripts/`.

This is the part that teaches OpenCode or Codex how to run the planner workflow.

### 2. Project-local artifacts

The actual planning outputs belong inside the target project repository, for example:

- `planning/tasks/`
- `specs/`

Those files are project state, not global user configuration.

## Important Path Rules

Do not install the skill into temporary directories such as `/tmp` or macOS paths under `/private/var/folders/...`.

Use stable locations only:

- this repository for the source of truth
- `~/.config/opencode/skill/...` or `~/.config/codex/skill/...` for global skill links
- the target project repository for generated planning artifacts

Temporary system paths are acceptable only as runtime scratch space for tools like TLC. They are not valid installation targets.

## For Future Agents

If you are installing VibeTLA for a user:

1. Prefer the one-liner installer: `curl -fsSL https://raw.githubusercontent.com/mikolaj92/VibeTLA/main/install.sh | bash`.
2. Keep the skill source in a stable local checkout such as `~/.local/share/vibetla`.
3. Link the skill into the user's config directory.
4. Use `./scripts/bootstrap_project.sh` in the target project repo when you need local planning directories.
5. Keep feature inputs and generated spec packs inside the target project repo.
6. Do not treat temp directories as durable storage.

In short: skill globally, artifacts locally, temp only at runtime.
