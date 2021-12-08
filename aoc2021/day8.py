from more_itertools import unzip, flatten
with open("inputs/day8.txt") as f:
    input_text = [x[:-1] for x in f.readlines()]


sign, output = unzip(map(lambda x: x.split("|"), input_text))
all_outputs = flatten(map(lambda x: x.split(), output))
print(len(list(filter(lambda x: len(x) in (2,3,4,7), all_outputs))))
