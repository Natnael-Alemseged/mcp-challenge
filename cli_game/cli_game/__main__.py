"""Interactive CLI wrapper for the guess-the-number game."""
from __future__ import annotations

import argparse
from typing import Optional, Tuple

from .game import Game

RANGES = {
    "easy": (1, 10, 5),
    "medium": (1, 100, 10),
    "hard": (1, 1000, 15),
}


def _resolve_range_and_attempts(
    difficulty: str,
    low: Optional[int],
    high: Optional[int],
    max_attempts: Optional[int],
) -> Tuple[int, int, int]:
    """Derive effective low/high/attempts from difficulty and optional overrides."""
    base_low, base_high, base_attempts = RANGES.get(difficulty, RANGES["medium"])

    eff_low = low if low is not None else base_low
    eff_high = high if high is not None else base_high
    eff_attempts = max_attempts if max_attempts is not None else base_attempts

    if eff_low >= eff_high:
        raise ValueError(f"low must be < high (got low={eff_low}, high={eff_high})")
    if eff_attempts <= 0:
        raise ValueError("max_attempts must be a positive integer")

    return eff_low, eff_high, eff_attempts


def play(
    difficulty: str = "medium",
    seed: int | None = None,
    *,
    low: Optional[int] = None,
    high: Optional[int] = None,
    max_attempts: Optional[int] = None,
) -> None:
    """Run an interactive game session."""
    try:
        low, high, attempts = _resolve_range_and_attempts(difficulty, low, high, max_attempts)
    except ValueError as e:
        # Configuration errors should be shown once and abort.
        print(f"Configuration error: {e}")
        return

    if seed is not None:
        import random

        random.seed(seed)

    g = Game(low, high, max_attempts=attempts)
    print(
        f"Guess the number between {low} and {high} "
        f"(difficulty: {difficulty}, max attempts: {g.max_attempts})"
    )

    try:
        while not g.is_over():
            remaining = g.max_attempts - g.attempts
            prompt = (
                f"[Attempts {g.attempts + 1}/{g.max_attempts} | "
                f"{remaining} remaining] Your guess (or 'q' to quit): "
            )
            s = input(prompt).strip()
            if s.lower() in ("q", "quit", "exit"):
                print("Goodbye.")
                return
            try:
                n = int(s)
            except ValueError:
                print("Please enter a whole number (e.g. 7).")
                continue
            try:
                res = g.guess(n)
            except ValueError:
                print(f"Please enter a number between {low} and {high}.")
                continue
            if res == "correct":
                print(f"🎉 Correct! You found it in {g.attempts} attempts.")
                return
            print("Too low." if res == "low" else "Too high.")
    except KeyboardInterrupt:
        print("\nInterrupted — exiting game.")
        return

    print(f"Game over — the number was {g.secret}.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        prog="python -m cli_game",
        description="Play a small guess-the-number game in your terminal",
    )
    p.add_argument(
        "-d",
        "--difficulty",
        choices=["easy", "medium", "hard"],
        default="medium",
        help="preset ranges: easy (1-10), medium (1-100), hard (1-1000)",
    )
    p.add_argument(
        "--low",
        type=int,
        default=None,
        help="override lower bound for the secret number (must be < high)",
    )
    p.add_argument(
        "--high",
        type=int,
        default=None,
        help="override upper bound for the secret number (must be > low)",
    )
    p.add_argument(
        "--max-attempts",
        type=int,
        default=None,
        help="override maximum number of attempts (must be positive)",
    )
    p.add_argument("--seed", type=int, default=None, help="set RNG seed (useful for testing)")
    args = p.parse_args()
    play(
        args.difficulty,
        args.seed,
        low=args.low,
        high=args.high,
        max_attempts=args.max_attempts,
    )
