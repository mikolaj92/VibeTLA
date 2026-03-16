# Architecture

VibeTLA is a spec-first planning layer that sits before code generation or manual implementation.

The main flow is:

1. Read a raw feature description.
2. Normalize it into a lightweight feature model.
3. Render a spec pack.
4. Check the generated TLA+ model with TLC.
5. Produce a compact bundle for an implementation agent.

The Python package in `tools/feature_spec/` owns the CLI and artifact generation.

The skill assets in `.opencode/skills/feature-spec-planner/` and `codex/skill/feature-spec-planner/` define how the planner agent should behave before any coding starts.
