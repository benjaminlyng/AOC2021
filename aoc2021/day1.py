from more_itertools import pairwise

with open("inputs/day1.txt") as f:
    depths = [int(x) for x in f.readlines()]

print(len([a - b for a, b in pairwise(depths) if a<b]))