#!./.venv/bin/python
import os
import time
from argparse import ArgumentParser
from collections import Counter
from importlib.metadata import entry_points, EntryPoint

from aocd.models import _load_users, NON_ANSWER, Puzzle
from aocd.post import PuzzlePart, submit
from aocd.runner import _timeout_wrapper, colored

YD = tuple[int, int]
NS_PER_S = 1_000_000_000
DEFAULT_TIMEOUT = 30
MARK_CORRECT = "✔"
MARK_INCORRECT = "✖"
MARK_UNKNOWN = "?"
MARK_SKIP = "-"
MARK_CORRECT_COLORED = colored(MARK_CORRECT, "green")
MARK_INCORRECT_COLORED = colored(MARK_INCORRECT, "red")
MARK_UNKNOWN_COLORED = colored(MARK_UNKNOWN, "magenta")
MARK_SKIP_COLORED = colored(MARK_SKIP, "yellow")


def colorize(s):
    return (
        s.replace(MARK_CORRECT, MARK_CORRECT_COLORED)
        .replace(MARK_INCORRECT, MARK_INCORRECT_COLORED)
        .replace(MARK_UNKNOWN, MARK_UNKNOWN_COLORED)
        .replace(MARK_SKIP, MARK_SKIP_COLORED)
    )


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

    def __str__(self):
        return f"({self.year},{self.day})"


class Plugin:
    def __init__(self, name: str, days: list[YD], solve: EntryPoint):
        self.name = name
        self.days = days
        self.solve = solve

    def __str__(self) -> str:
        return f"Plugin[{self.name}, {len(self.days)} days, {self.solve}]"


def _load_args(plugins, accounts, can_run):
    years = sorted({d.year for d in can_run})
    days = sorted({d.day for d in can_run})
    parser = ArgumentParser(
        description="AoC all - run many solvers against many inputs"
    )
    parser.add_argument(
        "-p",
        "--plugins",
        nargs="+",
        choices=plugins,
        # default=plugins,
        help="List of plugins (solvers) to evaluate, all by default.",
    )
    parser.add_argument(
        "-y",
        "--years",
        metavar=f"({years[0]}-{years[-1]})",
        type=int,
        nargs="+",
        choices=years,
        # default=years,
        help="AoC years to run, all by default",
    )
    parser.add_argument(
        "-d",
        "--days",
        metavar=f"({days[0]}-{days[-1]})",
        type=int,
        nargs="+",
        choices=days,
        # default=days,
        help="AoC days to run, all by default",
    )
    parser.add_argument(
        "-a",
        "--accounts",
        nargs="+",
        choices=accounts,
        # default=accounts,
        help="accounts to run each plugin with, all by default.",
    )
    parser.add_argument(
        "-s",
        "--no-submit",
        action="store_false",
        dest="autosubmit",
        help="disable autosubmit, new answers are submitted by default.",
    )
    return parser.parse_args()


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


def get_mark(puzzle: Puzzle, part: PuzzlePart, val, autosubmit: bool):
    if val in NON_ANSWER:
        return MARK_SKIP
    if getattr(puzzle, f"answered_{part}"):
        result = val == getattr(puzzle, f"answer_{part}")
    elif autosubmit:
        submit(
            val, part=part, day=puzzle.day, year=puzzle.year, reopen=False, quiet=True
        )
        result = getattr(puzzle, f"answered_{part}")
    else:
        return MARK_UNKNOWN
    return MARK_CORRECT if result else MARK_INCORRECT


def run_with_timeout(
    entry_point: EntryPoint,
    timeout: float,
    dt: float = 0.1,
    capture: bool = True,
    **kwargs,
) -> tuple[str, str, float, int, str]:
    t0 = time.time()
    func = entry_point.load()
    future = _timeout_wrapper(func, capture=capture, timeout=timeout, **kwargs)
    while not future.done():
        time.sleep(dt)
    walltime = time.time() - t0
    reporttime = 0
    try:
        result = future.result()
        if len(result) == 2:
            a, b = result
        elif len(result) == 3:
            a, b, reporttime = result
        else:
            raise TypeError("Solve must return a 2- or 3-tuple")
    except Exception as err:
        a = b = ""
        print(err)
        error = repr(err)[:100]
    else:
        error = ""
        # longest correct answer seen so far has been 57 chars
        # that was the first example data from 2019/12/9 (i.e. the quine)
        a = str(a)[:60]
        b = str(b)[:60]
    return a, b, walltime, reporttime, error


def format_time(t: float, conv: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    if t < timeout / 4:
        color = "green"
    elif t < timeout / 2:
        color = "yellow"
    else:
        color = "red"
    return colored(f"{t:{conv}}", color)


if __name__ == "__main__":
    plugins = _load_plugins()
    TOKENS = _load_users()
    to_run = _load_days(plugins)

    args = _load_args([p.name for p in plugins], [a for a in TOKENS], to_run)
    if args.plugins:
        keep = set(args.plugins)
        plugins = [p for p in plugins if p.name in keep]
        to_run = _load_days(plugins)
    if args.accounts:
        keep = set(args.accounts)
        TOKENS = {a: t for a, t in TOKENS.items() if a in keep}
    if args.years:
        keep = set(args.years)
        to_run = [d for d in to_run if d.year in keep]
    if args.days:
        keep = set(args.days)
        to_run = [d for d in to_run if d.day in keep]

    N_ACCOUNTS = len(TOKENS)
    W_ACCOUNT = max([len(p) for p in TOKENS])
    W_PLUGIN = max([len(p.name) for p in plugins])
    W_TITLE = max([len(d.title) for d in to_run]) + 1

    DIVIDER = colored(" | ", "white")
    W_DIVIDER = 3
    W_LEFT = W_TITLE + W_DIVIDER + W_PLUGIN
    RULE = colored(
        "=" * (W_LEFT + W_DIVIDER + len(TOKENS) * (W_ACCOUNT + W_DIVIDER) + 10), "white"
    )
    print(f"     {'':>{W_LEFT}}{DIVIDER}", end="")
    for a in TOKENS:
        print(f"{a:^{W_ACCOUNT}}{DIVIDER}", end="")
    print()
    last_year = None
    last_day = None
    for d in to_run:
        if d.year != last_year:
            ys = colored(str(d.year), "red")
            print(f"{ys} {RULE}")
            last_year = d.year
            last_day = None
        for p in plugins:
            if d.yd not in p.days:
                continue
            if d.day != last_day:
                ds = colored(f"{d.day:>4}", "green")
                print(f"{ds} {d.title:<{W_TITLE}}{DIVIDER}", end="")
                last_day = d.day
            else:
                print(f"{'':>4} {'':{W_TITLE + W_DIVIDER}}", end="")
            print(f"{p.name:>{W_PLUGIN}}{DIVIDER}", end="")
            total_wall = 0
            total_report = 0
            for token in TOKENS.values():
                puzzle = d.get_puzzle(token)
                a, b, walltime, reporttime, error = run_with_timeout(
                    entry_point=p.solve,
                    timeout=DEFAULT_TIMEOUT,
                    year=d.year,
                    day=d.day,
                    data=puzzle.input_data,
                )
                total_wall += walltime
                if reporttime is not None:
                    total_report += reporttime / NS_PER_S
                if error:
                    if error.startswith("TimeoutError("):
                        a = b = None
                        mark = "t/o"
                    else:
                        print(f"Error retrieving answers: {error}")
                        exit(1)
                else:
                    mark = get_mark(puzzle, "a", a, args.autosubmit)
                    if not d.is_last_day:
                        if mark == MARK_UNKNOWN:
                            mark += MARK_UNKNOWN
                        else:
                            mark += get_mark(puzzle, "b", b, args.autosubmit)
                mark_stats.update(mark)
                print(colorize(f"{mark:^{W_ACCOUNT}}{DIVIDER}"), end="")
            if total_report == 0:
                print(
                    colored("[", "white")
                    + format_time(total_wall / len(TOKENS), "6.2f")
                    + colored(" s]", "white")
                )
            else:
                print(
                    format_time(total_report / len(TOKENS), "8.3f")
                    + colored("s", "white")
                )
    if MARK_INCORRECT in mark_stats:
        print(f"¡¡ {mark_stats[MARK_INCORRECT]} incorrect !!")
    if MARK_SKIP in mark_stats:
        print(f"{mark_stats[MARK_SKIP]} skipped")
    if MARK_UNKNOWN in mark_stats:
        print(f"{mark_stats[MARK_UNKNOWN]} unknown (not submitted)")
