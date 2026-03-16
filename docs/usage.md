# Usage

## Setup

```bash
mise install
uv sync
```

## Create a planning pack from a task file

```bash
uv run feature-spec plan planning/tasks/example-session-refresh.md
```

## Create a planning pack from raw text

```bash
uv run feature-spec plan --from-text "Add session refresh with bounded retry"
```

## Check a generated spec

```bash
uv run feature-spec check specs/example-session-refresh
```

`check` requires `java` and `tla2tools.jar`. The runner looks for the jar in:

1. `TLATOOLS_JAR`
2. `TLA2TOOLS_JAR`
3. `~/.local/share/tla2tools.jar`
4. `~/tla2tools.jar`
5. `/opt/tla2tools.jar`
6. `/usr/local/share/tla2tools.jar`
7. `./tla2tools.jar`

## Rebuild the machine-readable bundle

```bash
uv run feature-spec bundle specs/example-session-refresh
```

## Check the local environment

```bash
uv run feature-spec doctor
```
