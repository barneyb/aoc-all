def support():
    return [(2015, 1)]


def solve(year, day, data):
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
