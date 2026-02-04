CLI Guess-the-number game

Run locally:

  python -m cli_game

Options:
  -d/--difficulty   easy|medium|hard   (default: medium; sets base range & attempts)
  --low <int>       override lower bound for the secret number
  --high <int>      override upper bound for the secret number
  --max-attempts<n> override max number of attempts
  --seed <int>      deterministic secret (useful for testing)

Examples:

  # Default medium game
  python -m cli_game

  # Easier, smaller range
  python -m cli_game -d easy

  # Custom range and attempts
  python -m cli_game --low 10 --high 50 --max-attempts 8

Run tests (uses stdlib unittest):

  python -m unittest discover -s cli_game/tests -p "test_*.py" -v

Ideas for improvements: leaderboard, configurable ranges, nicer CLI UX.
