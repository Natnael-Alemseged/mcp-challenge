## Improve CLI guess-the-number tool

### Goals
- Keep the existing `Game` logic intact and fully compatible with current tests.
- Make the CLI wrapper more ergonomic and robust for end users.
- Document any new behavior in the CLI README.

### Planned changes
- **CLI UX improvements**
  - Show remaining attempts more clearly in the prompt.
  - Handle `KeyboardInterrupt` (Ctrl+C) gracefully instead of showing a stack trace.
  - Slightly refine messages for invalid input while preserving simple text output.
- **Configurability**
  - Extend the existing `argparse` interface in `__main__.py` to support optional `--low`, `--high`, and `--max-attempts` flags.
  - When these flags are provided, they should override the chosen difficulty preset, with validation that `low < high` and attempts is positive.
- **Documentation & verification**
  - Update `cli_game/README.md` to describe the new flags with short examples.
  - Run the existing unittest suite and, if needed, add or adjust tests that cover any logic we touch outside of pure I/O.

### Non-goals / constraints
- Do not change the public API or semantics of the `Game` class.
- Avoid adding external dependencies; stick to the Python standard library.

