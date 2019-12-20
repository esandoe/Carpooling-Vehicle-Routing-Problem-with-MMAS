import math
from typing import *


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges: Dict[int, Dict[Node, Edge]] = {}

        self.dropoff: Union[Node, None] = None
        self.visited: bool = False


class Edge:
    max_pheromones = 100
    min_pheromones = 0.5
    evaporation_rate = 0.98

    def __init__(self, from_node, to_node, cost):
        self.from_node: Node = from_node
        self.to_node: Node = to_node
        self.cost: float = cost

        self.pheromones: float = self.max_pheromones

    def add_pheromones(self, pheromones):
        self.pheromones += pheromones

        if self.pheromones > self.max_pheromones:
            self.pheromones = self.max_pheromones

    def evaporation(self):
        self.pheromones *= self.evaporation_rate

        if self.pheromones < self.min_pheromones:
            self.pheromones = self.min_pheromones


def distance(p: Node, q: Node):
    return math.sqrt((q.x - p.x) ** 2 + (q.y - p.y) ** 2)


def create_graph_from_data(data, N: int):
    start = data[0]
    start_node = Node(start[0], start[1])

    nodes = []
    for (x1, y1), (x2, y2) in data[1:]:
        p = Node(x1, y1)
        q = Node(x2, y2)
        p.dropoff = q
        nodes.append(p)
        nodes.append(q)

    start_node.edges = create_edges(start_node, nodes, N)

    for node in nodes:
        node.edges = create_edges(node, nodes, N)

    edges = []
    for node in nodes + [start_node]:
        for n in range(N):
            edges += list(node.edges[n].values())

    return start_node, nodes, edges


def create_edges(from_node, nodes, N: int):
    edges = dict.fromkeys(range(N))
    for n in range(N):
        edges[n] = {}
    for to_node in nodes:
        if from_node != to_node:
            cost = distance(from_node, to_node)
            for n in range(N):
                edges[n][to_node] = Edge(from_node, to_node, cost)
    return edges
