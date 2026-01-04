#!./.venv/bin/python

import os
from collections import Counter
from importlib.metadata import entry_points, EntryPoint

from aocd.models import _load_users, NON_ANSWER, Puzzle
from aocd.post import PuzzlePart, submit
from aocd.runner import format_time, run_with_timeout

YD = (int, int)
MARK_CORRECT = "✔"
MARK_INCORRECT = "✖"
MARK_SKIP = "-"

mark_stats = Counter()


class Day:
    def __init__(self, year: int, day: int):
        self.year = year
        self.day = day
        self.title = Puzzle(year, day).title

    def get_puzzle(self, token: str) -> Puzzle:
        os.environ["AOC_SESSION"] = token
        return Puzzle(self.year, self.day)

    def __getattr__(self, item):
        if item == "yd":
            return self.year, self.day
        if item == "is_last_day":
            return self.day == 25 if self.year < 2025 else self.day == 12
        raise AttributeError


class Plugin:
    def __init__(self, name: str, days: list[YD], solve: EntryPoint):
        self.name = name
        self.days = days
        self.solve = solve

    def __str__(self) -> str:
        return f"Plugin[{self.name}, {len(self.days)} days, {self.solve}]"


def _load_plugins() -> list[Plugin]:
    plugins_by_name = dict()
    for ep in entry_points(group="barneyb_aoc_all.support"):
        support = ep.load()
        name = ep.name
        if name in plugins_by_name:
            raise RuntimeError(f"Multiple entry points named '{name}' found")
        ep = entry_points(group="barneyb_aoc_all.solve", name=name)
        if len(ep) == 0:
            raise RuntimeError(f"No solve entry point found for '{name}'")
        if len(ep) > 1:
            raise RuntimeError(f"Found {len(ep)} solve entry points for '{name}'")
        (ep,) = ep
        plugins_by_name[name] = Plugin(name, support(), ep)
    return sorted(plugins_by_name.values(), key=lambda p: p.name)


def _load_days(plugins: list[Plugin]) -> list[Day]:
    to_run = set()
    for p in plugins:
        to_run.update(p.days)
    to_run = [Day(y, d) for (y, d) in to_run]
    to_run.sort(key=lambda d: d.year * 100 + d.day, reverse=True)
    return to_run


def check_answer(puzzle: Puzzle, part: PuzzlePart, val):
    if val in NON_ANSWER:
        return None
    if getattr(puzzle, f"answered_{part}"):
        return val == getattr(puzzle, f"answer_{part}")
    submit(val, part=part, day=puzzle.day, year=puzzle.year, reopen=False, quiet=True)
    return getattr(puzzle, f"answered_{part}")


def get_mark(good: bool) -> str:
    return MARK_CORRECT if good else MARK_SKIP if good is None else MARK_INCORRECT


if __name__ == "__main__":
    TOKENS = _load_users()
    N_ACCOUNTS = len(TOKENS)
    W_ACCOUNT = max([len(p) for p in TOKENS])

    plugins = _load_plugins()
    W_PLUGIN = max([len(p.name) for p in plugins])

    to_run = _load_days(plugins)
    W_TITLE = max([len(d.title) for d in to_run]) + 1

    DIVIDER = " | "
    W_LEFT = W_TITLE + len(DIVIDER) + W_PLUGIN
    RULE = "=" * (W_LEFT + len(DIVIDER) + len(TOKENS) * (W_ACCOUNT + len(DIVIDER)) - 1)
    print(f"     {'':>{W_LEFT}}{DIVIDER}", end="")
    for a in TOKENS:
        print(f"{a:^{W_ACCOUNT}}{DIVIDER}", end="")
    print()
    last_year = None
    last_day = None
    for d in to_run:
        if d.year != last_year:
            print(f"{d.year} {RULE}")
            last_year = d.year
            last_day = None
        for p in plugins:
            if d.yd not in p.days:
                continue
            if d.day != last_day:
                print(f"{d.day:>4} {d.title:<{W_TITLE}}{DIVIDER}", end="")
                last_day = d.day
            else:
                print(f"{'':>4} {'':{W_TITLE + len(DIVIDER)}}", end="")
            print(f"{p.name:>{W_PLUGIN}}{DIVIDER}", end="")
            total_time = 0
            for token in TOKENS.values():
                puzzle = d.get_puzzle(token)
                a, b, walltime, error = run_with_timeout(
                    entry_point=p.solve,
                    timeout=30,
                    year=d.year,
                    day=d.day,
                    data=puzzle.input_data,
                    progress=None,
                    capture=True,
                )
                total_time += walltime
                if error:
                    if error.startswith("TimeoutError("):
                        a = b = None
                        mark = "t/o"
                    else:
                        print(f"Error retrieving answers: {error}")
                        exit(1)
                else:
                    mark = get_mark(check_answer(puzzle, "a", a))
                    if not d.is_last_day:
                        mark += get_mark(check_answer(puzzle, "b", b))
                mark_stats.update(mark)
                print(f"{mark:^{W_ACCOUNT}}{DIVIDER}", end="")
            print(format_time(total_time / len(TOKENS), 15))
    if MARK_INCORRECT in mark_stats:
        print(f"¡¡ {mark_stats[MARK_INCORRECT]} incorrect !!")
    elif MARK_SKIP in mark_stats:
        print(f"{mark_stats[MARK_SKIP]} skipped")
