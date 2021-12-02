with open("inputs/day2.txt") as f:
    course = f.readlines()
    
directions = {'up':0, 'down':0, 'forward':0}
for c in course:
    cmd, val = c.split()
    directions[cmd] += int(val)

print((directions['down'] - directions['up'])* directions['forward'])

# Part 2
directions = {'depth':0, 'forward':0, "aim":0}
for c in course:
    cmd, val = c.split()
    val = int(val)
    if cmd == 'up':
        directions['aim'] -= val
    elif cmd == 'down':
        directions['aim'] += val
    else:
        directions[cmd] += val
        directions["depth"] += val*directions['aim']

print((directions['depth'])* directions['forward'])
