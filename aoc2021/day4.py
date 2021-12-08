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
for i in range(1, int(len(boards) ), 6):
    all_boards.append([board.split() for board in boards[i : i + 5]])


def insert_board(board):
    nodes = board.copy()
    for row in nodes:
        for i, number in enumerate(row):
            row[i] = Node(label="number", properties={"value": int(number), "marked":"False"})
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
        MATCH (a1) -[:horizontal] ->(a2) -[:horizontal]->(a3) -[:horizontal]->(a4) -[:horizontal] ->(a5)
        where a1.marked=True and a2.marked=True and a3.marked=True and a4.marked=True and a5.marked=True 
        RETURN id(a1) as id
        UNION all
        MATCH (o1) -[:vertical] ->(o2) -[:vertical]->(o3) -[:vertical]->(o4) -[:vertical] ->(o5)
        where o1.marked=True and o2.marked=True and o3.marked=True and o4.marked=True and o5.marked=True 
        RETURN id(o1) as id
        """
    result = redis_graph.query(q)
    if n == '24':
        print(result.result_set)

    if result.result_set:
        q = """
            MATCH (o) - [*] - (n)
            where id(o)=$result
            with distinct(n) as n
            MATCH (o)
            where  n.marked<>True
            with distinct(n) as n
            return sum(n.value)
            """
        result = redis_graph.query(q, {"result":int(result.result_set[0][0])})
        print(result.result_set[0][0]*int(n))
        break

    
