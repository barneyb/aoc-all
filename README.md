# Advent of Code - Solve All

Make sure you have Python 3.11 or better, and you have [advent-of-code-data](https://github.com/wimglenn/advent-of-code-data?tab=readme-ov-file#quickstart) set up with your token(s). Then, from the root:

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install . ./sample
./run.py
```

I have two tokens configured, so it yields output like this:

```
                              | github | gmail  | 
2015 ============================================
   1 Not Quite Lisp  | sample |   ✔✖   |   ✔✖   |    0.42s
```

Part b is not implemented, and so marked wrong. Note that the time is for the entire row, including some per token overhead. It'll tell you if your solution's slow, but won't confirm you've shaved off that last few milliseconds. If your solver takes more than 15 seconds, it'll time out and be reported as `t/o`. Also note that all output from your solver is sent to `/dev/null`.

The `sample` folder is an example of how to set up a plugin and is what is running above. It can solve the very first [Advent of Code](https://adventofcode.com) puzzle: [Not Quite Lisp](https://adventofcode.com/2015/day/1).

The `barneyb_aoc_all.support` entry point must resolve to a zero-arg function which returns a sequence of two-tuples, each a year and day which your plugin can solve. The sample returns `[(2015, 1)]`, as you'd expect.

The `barneyb_aoc_all.solve` entry point must resolve to a three-arg function which accepts `year`, `day`, and `data` (contents of `input.txt`), and returns a pair of answers. Use `None` or `""` if you don't know one of them (yet). Normally this function would use the first two args to delegate to "something", passing along `data` for it to use, but the sample only solves that single puzzle.

When you're ready to go for real, install some more plugins:

```
python3 -m pip install ../aoc-2025
python3 -m pip install ../aoc-2024
```
