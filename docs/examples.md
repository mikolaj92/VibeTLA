# Examples

The repository includes one example task in `planning/tasks/example-session-refresh.md` and one example spec pack in `specs/example-session-refresh/`.

Use the example task when you want to see the v1 flow end to end:

```bash
uv run feature-spec plan planning/tasks/example-session-refresh.md
uv run feature-spec check specs/example-session-refresh
uv run feature-spec bundle specs/example-session-refresh
```

The resulting pack includes:
- `plan.md`
- `spec.tla`
- `model.cfg`
- `impl.md`
- `tests.md`
- `bundle.json`
