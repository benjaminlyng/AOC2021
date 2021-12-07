import redis
from more_itertools import pairwise
from redisgraph import Node, Edge, Graph

with open("inputs/day4.txt") as f:
    input_text = f.readlines()
draws, *boards = input_text

r = redis.Redis(host="localhost", port=6379)

redis_graph = Graph("Bingo", r)
try:
    redis_graph.delete()
except:
    pass
all_boards = []
for i in range(1, int(len(boards) / 6), 6):
    all_boards.append([board.split() for board in boards[i : i + 5]])


def insert_board(board):
    nodes = board.copy()
    for row in nodes:
        for i, number in enumerate(row):
            row[i] = Node(label="number", properties={"value": int(number)})
            redis_graph.add_node(row[i])
    for row in nodes:
        for a, b in pairwise(row):
            redis_graph.add_edge(Edge(a, "vertical", b))
    for row in zip(*nodes):
        for a, b in pairwise(row):
            redis_graph.add_edge(Edge(a, "horizontal", b))


for board in all_boards:
    insert_board(board)

redis_graph.commit()

for n in draws.split(","):
    q = f"""
        MATCH (o:number {{value:{int(n)}}})
        set o.marked=True
        return o
        """
    redis_graph.query(q)
    q = f"""
        unwind ['vertical', 'horizontal'] as direction
        MATCH (o1:number) -[:directions] -(o2:number) -[:directions]-(o3:number) -[:directions]-(o4:number) -[:directions] -(o5:number) 
        
        return o1
        """
    result = redis_graph.query(q)
    if result.result_set:
        print(result.result_set)

    
