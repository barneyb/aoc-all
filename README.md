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
   1 Not Quite Lisp  | sample |   ✔-   |   ✔-   |    0.42s
2 skipped
```

Part b is not implemented, and so marked skipped. Note that the time is an average - not the total - for the row's solutions, and includes process overhead. It'll tell you if your solver's slow, but won't confirm you've shaved off that last few tens of milliseconds. If your solver takes more than 30 seconds, it'll time out and be reported as `t/o`. Also note that any output from your solver is sent to `/dev/null`.

The `sample` folder is an example of how to set up a plugin and is what is running above. It can solve the very first [Advent of Code](https://adventofcode.com) puzzle: [Not Quite Lisp](https://adventofcode.com/2015/day/1).

The `barneyb_aoc_all.support` entry point must resolve to a zero-arg function which returns a sequence of two-tuples, each a year and day which your plugin can solve. The sample returns `[(2015, 1)]`, as you'd expect.

The `barneyb_aoc_all.solve` entry point must resolve to a three-arg function which accepts `year`, `day`, and `data` (contents of `input.txt`), and returns a pair of answers. Use `None` or `""` if you don't know one of them (yet). Normally this function would use the first two args to delegate to "something", passing along `data` for it to use, but the sample only solves that single puzzle.

A real example, for my 2023 solvers, can be found at https://github.com/barneyb/aoc-2023/blob/master/python/pyproject.toml. It has two entry points, one for Python implementations and one for Java implementations, which I'd mashed into the same repo. After installing, run with some filters:

```
% python3 -m pip install ../aoc-2023/python
% ./run.py -y 2023 2022 2015 -d 1 2 24 -a gmail
                                                   | gmail |
2023 =======================================================
  24 Never Tell Me The Odds             |   java23 |  ✔✔   |    1.37s
                                          python23 |  ✔-   |    0.21s
   2 Cube Conundrum                     | python23 |  ✔✔   |    0.21s
   1 Trebuchet?!                        | python23 |  ✔✔   |    0.21s
2022 =======================================================
   1 Calorie Counting                   | python23 |  ✔✔   |    0.21s
2015 =======================================================
   2 I Was Told There Would Be No Math  |   java23 |  ✔✔   |    1.05s
   1 Not Quite Lisp                     |   java23 |  ✔✔   |    1.14s
                                          python23 |  ✔✔   |    0.20s
                                            sample |  ✔-   |    0.21s
2 skipped
```

This illustrates the process overhead. The Java solvers are indirected through two layers of spawned processes, pass through Maven, and use filesystem IO for input passing. _Not Quite Lisp_ only takes a couple milliseconds to run, so there's a full second of overhead.
