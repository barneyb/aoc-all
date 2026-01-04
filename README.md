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

A real example, for my 2023 solvers, can be found at https://github.com/barneyb/aoc-2023/blob/master/python/pyproject.toml. It has two entry points, one for Python implementations and one for Java implementations, which I'd mashed into the same repo. I installed it with:

```
python3 -m pip install ../aoc-2023/python
```

Running now yields output like this:

```
                                                         | github | gmail  |
2023 =======================================================================
  25 Snowverload                              | python23 |   ✔    |   ✔    |    0.56s
  24 Never Tell Me The Odds                   |   java23 |   ✔✔   |   ✔✔   |    1.14s
                                                python23 |   ✔-   |   ✔-   |    0.21s
  23 A Long Walk                              | python23 |   ✔✔   |   ✔✔   |    6.80s
  22 Sand Slabs                               | python23 |   ✔✔   |   ✔✔   |    0.20s
  21 Step Counter                             |   java23 |   ✔✔   |   ✔✔   |    2.24s
                                                python23 |   ✔-   |   ✔-   |    0.21s
  20 Pulse Propagation                        | python23 |   ✔✔   |   ✔✔   |    0.21s
  19 Aplenty                                  | python23 |   ✔✔   |   ✔✔   |    0.21s
  18 Lavaduct Lagoon                          | python23 |   ✔✔   |   ✔✔   |    0.21s
  17 Clumsy Crucible                          | python23 |   ✔✔   |   ✔✔   |   11.74s
  16 The Floor Will Be Lava                   | python23 |   ✔✔   |   ✔✔   |    1.97s
  15 Lens Library                             | python23 |   ✔✔   |   ✔✔   |    0.21s
  14 Parabolic Reflector Dish                 | python23 |   ✔✔   |   ✔✔   |    1.87s
  13 Point of Incidence                       | python23 |   ✔✔   |   ✔✔   |    0.21s
  12 Hot Springs                              | python23 |   ✔✔   |   ✔✔   |    0.32s
  11 Cosmic Expansion                         | python23 |   ✔✔   |   ✔✔   |    0.21s
  10 Pipe Maze                                | python23 |   ✔✔   |   ✔✔   |    0.21s
   9 Mirage Maintenance                       |   java23 |   ✔✔   |   ✔✔   |    1.08s
                                                python23 |   ✔✔   |   ✔✔   |    0.21s
   8 Haunted Wasteland                        | python23 |   ✔✔   |   ✔✔   |    0.21s
   7 Camel Cards                              | python23 |   ✔✔   |   ✔✔   |    0.21s
   6 Wait For It                              | python23 |   ✔✔   |   ✔✔   |    0.21s
   5 If You Give A Seed A Fertilizer          | python23 |   ✔✔   |   ✔✔   |    0.20s
   4 Scratchcards                             | python23 |   ✔✔   |   ✔✔   |    0.21s
   3 Gear Ratios                              | python23 |   ✔✔   |   ✔✔   |    0.21s
   2 Cube Conundrum                           | python23 |   ✔✔   |   ✔✔   |    0.20s
   1 Trebuchet?!                              | python23 |   ✔✔   |   ✔✔   |    0.21s
2022 =======================================================================
  12 Hill Climbing Algorithm                  | python23 |   ✔✔   |   ✔✔   |    0.56s
   5 Supply Stacks                            |   java23 |   ✔✔   |   ✔✔   |    1.09s
   1 Calorie Counting                         | python23 |   ✔✔   |   ✔✔   |    0.21s
2021 =======================================================================
  14 Extended Polymerization                  | python23 |   ✔✔   |   ✔✔   |    0.21s
  11 Dumbo Octopus                            | python23 |   ✔✔   |   ✔✔   |    0.21s
   5 Hydrothermal Venture                     |   java23 |   ✔✔   |   ✔✔   |    1.18s
2020 =======================================================================
  17 Conway Cubes                             | python23 |   ✔✔   |   ✔✔   |    1.04s
  10 Adapter Array                            | python23 |   ✔✔   |   ✔✔   |    0.21s
   5 Binary Boarding                          |   java23 |   ✔✔   |   ✔✔   |    1.05s
2019 =======================================================================
   8 Space Image Format                       | python23 |   ✔✔   |   ✔✔   |    0.21s
   6 Universal Orbit Map                      | python23 |   ✔✔   |   ✔✔   |    0.21s
   5 Sunny with a Chance of Asteroids         |   java23 |   ✔✔   |   ✔✔   |    1.12s
   2 1202 Program Alarm                       |   java23 |   ✔✔   |   ✔✔   |    1.13s
2018 =======================================================================
  18 Settlers of The North Pole               | python23 |   ✔✔   |   ✔✔   |    2.72s
  12 Subterranean Sustainability              | python23 |   ✔✔   |   ✔✔   |    0.21s
   5 Alchemical Reduction                     |   java23 |   ✔✔   |   ✔✔   |    1.13s
   1 Chronal Calibration                      | python23 |   ✔✔   |   ✔✔   |    0.20s
2017 =======================================================================
  17 Spinlock                                 | python23 |   ✔✔   |   ✔✔   |    3.38s
  13 Packet Scanners                          | python23 |   ✔✔   |   ✔✔   |    1.14s
   7 Recursive Circus                         |   java23 |   ✔✔   |   ✔✔   |    1.14s
   5 A Maze of Twisty Trampolines, All Alike  |   java23 |   ✔✔   |   ✔✔   |    1.14s
   1 Inverse Captcha                          | python23 |   ✔✔   |   ✔✔   |    0.21s
2016 =======================================================================
  16 Dragon Checksum                          | python23 |   ✔✔   |   ✔✔   |    2.72s
  10 Balance Bots                             | python23 |   ✔✔   |   ✔✔   |    0.21s
   9 Explosives in Cyberspace                 | python23 |   ✔✔   |   ✔✔   |    0.21s
   8 Two-Factor Authentication                | python23 |   ✔✔   |   ✔✔   |    0.21s
   7 Internet Protocol Version 7              | python23 |   ✔✔   |   ✔✔   |    0.23s
   5 How About a Nice Game of Chess?          |   java23 |   ✔✔   |   ✔✔   |    8.93s
   4 Security Through Obscurity               |   java23 |   ✔✔   |   ✔✔   |    1.13s
   2 Bathroom Security                        |   java23 |   ✔✔   |   ✔✔   |    1.09s
   1 No Time for a Taxicab                    |   java23 |   ✔✔   |   ✔✔   |    1.05s
                                                python23 |   ✔✔   |   ✔✔   |    0.21s
2015 =======================================================================
  15 Science for Hungry People                | python23 |   ✔✔   |   ✔✔   |    0.91s
  10 Elves Look, Elves Say                    | python23 |   ✔✔   |   ✔✔   |    1.52s
   2 I Was Told There Would Be No Math        |   java23 |   ✔✔   |   ✔✔   |    1.05s
   1 Not Quite Lisp                           |   java23 |   ✔✔   |   ✔✔   |    1.04s
                                                python23 |   ✔✔   |   ✔✔   |    0.21s
4 skipped
```
