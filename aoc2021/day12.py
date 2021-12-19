import redis
from more_itertools import pairwise
from redisgraph import Edge, Graph, Node
from more_itertools import one

with open("inputs/day12-example.txt") as f:
    input_text = [x[:-1] for x in f.readlines()]


edges = tuple(map(lambda x: x.split("-"), input_text))

r = redis.Redis(host="localhost", port=6379)

redis_graph = Graph("caves", r)
try:
    redis_graph.delete()
except:
    pass


def create_path(graph: Graph, p1, p2):
    q = """MERGE (o:cave {name:$p1})
        MERGE (p:cave {name:$p2})
        MERGE (o) -[:tunnel] - (p)
        """
    graph.query(q, params={"p1": p1, "p2": p2})


for p1, p2 in edges:
    create_path(redis_graph, p1, p2)

q = """
    MATCH p=( {name:"start"}) - [*] - ({name:"end"})
    Return [node IN nodes(p) | node.name] as path
    """
result = redis_graph.query(q)
paths = list(map(one, result.result_set))
print(paths)
