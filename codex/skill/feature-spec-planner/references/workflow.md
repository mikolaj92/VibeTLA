# workflow

1. Write a structured task file in the target repository.
2. From the stable VibeTLA checkout, run `uv run feature-spec plan <target-task-path> --output-root <target-repo>/specs`.
3. Run `uv run feature-spec check <target-spec-directory>`.
4. Run `uv run feature-spec bundle <target-spec-directory>`.
5. Hand off the checked bundle to the implementation agent.

Never write `spec.tla` manually. If the CLI or TLC is unavailable, run `uv run feature-spec doctor` and stop on failure. Never paper over ambiguity with fallback behavior.
