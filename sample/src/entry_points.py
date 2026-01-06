def support():
    return [(2015, 1)]


def solve(year, day, data):
    if year != 2015 or day != 1:
        raise TypeError("Only 2015 day 1 is supported")

    # return not_quite_lisp(data)

    # Alternatively, use a solver-reported time:
    #
    import time

    start = time.time_ns()
    a, b = not_quite_lisp(data)
    return a, b, time.time_ns() - start


def not_quite_lisp(data):
    # Normally this entry point would use year/day to delegate to that day's
    # solver, in some fashion or another. But since it's hard-coded to only
    # support one single problem, there's no need.
    floor = 0
    for c in data:
        if c == "(":
            floor += 1
        elif c == ")":
            floor -= 1
    return floor, None
