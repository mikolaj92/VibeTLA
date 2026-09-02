# Usage

## Setup

```bash
mise install
uv sync
```

## Create a new planning pack

Use a structured task with non-empty `## States` and `## Transitions`. The output directory must not already contain a pack.

```bash
uv run feature-spec plan /path/to/target/planning/tasks/new-feature.md --output-root /path/to/target/specs
```

`--from-text` accepts the same structured Markdown and fails closed on loose prose:

```bash
uv run feature-spec plan --from-text $'## States\n- idle\n- ready\n## Transitions\n- activate: idle -> ready' --task-id new-feature --output-root /path/to/target/specs
```

## Check and bundle the committed example

```bash
uv run feature-spec check specs/example-session-refresh
uv run feature-spec bundle specs/example-session-refresh
```

`check` requires `java` and `tla2tools.jar`. Run `uv run feature-spec doctor` for the exact environment report. The runner checks `TLATOOLS_JAR`, `TLA2TOOLS_JAR`, standard user/system locations, and `./tla2tools.jar`.
