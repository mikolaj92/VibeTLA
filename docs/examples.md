# Examples

The repository includes one checked example task in `planning/tasks/example-session-refresh.md` and its committed pack in `specs/example-session-refresh/`.

Validate and rebuild the committed example without overwriting it:

```bash
uv run feature-spec check specs/example-session-refresh
uv run feature-spec bundle specs/example-session-refresh
```

To exercise `plan`, create a new task id in a target repository. The destination must not already contain a non-empty pack:

```bash
uv run feature-spec plan /path/to/target/planning/tasks/new-session-flow.md --output-root /path/to/target/specs
```

The resulting pack includes `plan.md`, `spec.tla`, `model.cfg`, `impl.md`, `tests.md`, and `bundle.json`.
