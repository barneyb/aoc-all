# Advent of Code - Solve All

Make sure you have Python 3.11 or better, and you have [advent-of-code-data](https://github.com/wimglenn/advent-of-code-data?tab=readme-ov-file#quickstart) (this project's inspiration) set up with your token(s). Then, from the root:

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
   1 Not Quite Lisp  | sample |   ✔-   |   ✔-   | [  0.21 s]
2 skipped
```

Part b is not implemented, and so marked skipped. Note that the time is an average - not the total - for the row's solutions, and includes process overhead out of the box. It'll tell you if your solver's slow, but won't confirm you've shaved off that last few tens of milliseconds. If your solver takes more than 30 seconds, it'll time out and be reported as `⧖`. Also note that your solvers' `STDOUT` is sent to `/dev/null`.

The `sample` folder is an example of how to set up a plugin and is what is running above. It can solve part A of the very first AoC puzzle: [Not Quite Lisp](https://adventofcode.com/2015/day/1).

The `barneyb_aoc_all.support` entry point must resolve to a zero-arg function which returns a sequence of pairs, each a year and day which your plugin can solve. The sample returns `[(2015, 1)]`, as you'd expect.

The `barneyb_aoc_all.solve` entry point must resolve to a three-arg function which accepts `year`, `day`, and `data` (contents of `input.txt`), and returns a pair of answers. Use `None` or `""` if you don't know one of them (yet). If you don't like the process overhead in the reported times, you can optionally return a triple instead of a pair, where the third element is runtime to report _in nanoseconds_.

A real example, for my 2023 solvers, can be found at https://github.com/barneyb/aoc-2023/blob/master/python/pyproject.toml. It has two entry points, one for Python solvers and one for Java solvers, which I'd mashed into the same repo. After installing, run with some filters:

```
% python3 -m pip install ../aoc-2023/python
% ./run.py -y 2023 2022 2015 -d 1 2 24 -a gmail
                                                   | gmail |
2023 =======================================================
  24 Never Tell Me The Odds             |   java23 |  ✔✔   | [  1.05 s]
                                          python23 |  ✔-   | [  0.21 s]
   2 Cube Conundrum                     | python23 |  ✔✔   | [  0.20 s]
   1 Trebuchet?!                        | python23 |  ✔✔   | [  0.20 s]
2022 =======================================================
   1 Calorie Counting                   | python23 |  ✔✔   | [  0.21 s]
2015 =======================================================
   2 I Was Told There Would Be No Math  |   java23 |  ✔✔   | [  1.15 s]
   1 Not Quite Lisp                     |   java23 |  ✔✔   | [  1.01 s]
                                          python23 |  ✔✔   | [  0.20 s]
                                            sample |  ✔-   | [  0.20 s]
2 skipped
```

This illustrates the process overhead. The Java solvers are indirected through two layers of spawned processes, pass through Maven, and use filesystem IO for input passing. _Not Quite Lisp_ only takes a millisecond to run, so there's a full second of overhead.

I added solver-reported timing for both 2023 plugins, which doesn't change how long `./run.py` takes, but gives a truer report. Note that solver-reported times have one more fractional digit and lack brackets. As solver-reported and runner-measured times are not directly comparable, this hints at where you need to squint a little.

```
% ./run.py -y 2023 2022 2015 -d 1 2 24 -a gmail
                                                   | gmail |
2023 =======================================================
  24 Never Tell Me The Odds             |   java23 |  ✔✔   |    0.014s
                                          python23 |  ✔-   |    0.015s
   2 Cube Conundrum                     | python23 |  ✔✔   |    0.002s
   1 Trebuchet?!                        | python23 |  ✔✔   |    0.002s
2022 =======================================================
   1 Calorie Counting                   | python23 |  ✔✔   |    0.001s
2015 =======================================================
   2 I Was Told There Would Be No Math  |   java23 |  ✔✔   |    0.002s
   1 Not Quite Lisp                     |   java23 |  ✔✔   |    0.001s
                                          python23 |  ✔✔   |    0.001s
                                            sample |  ✔-   | [  0.20 s]
2 skipped
```
