from more_itertools import pairwise
from more_itertools import triplewise

with open("inputs/day1.txt") as f:
    depths = [int(x) for x in f.readlines()]

print(len([True for a, b in pairwise(depths) if a < b]))

bins = [a + b + c for a, b, c in triplewise(depths)]
print(len([True for a, b in pairwise(bins) if a < b]))
