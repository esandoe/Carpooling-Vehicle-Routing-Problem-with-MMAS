import random
import operator
from typing import *

from Graph import *


class Ant:
    q = 0
    b = 6
    R = 10
    capacity = 16

    def __init__(self, start_node: Node, num: int):
        self.route: List[Edge] = []
        self.current_node = start_node
        self.passengers_on_board: List[Node] = []
        self.total_passenger_time = 0
        self.num = num

    def walk(self) -> Union[Edge, None]:
        edge = self.next(self.current_node)  # select the next node using the transition function

        if edge is None:
            return None

        # Count passenger time (passenger cost?) for the visited edge
        self.total_passenger_time += edge.cost * (len(self.passengers_on_board) + Ant.R)

        self.current_node = edge.to_node
        self.route.append(edge)

        if len(self.route) is not 0:
            if self.current_node.dropoff is None:
                # If the visited edge leads to a dropoff node, remove the passenger and the node
                self.passengers_on_board.remove(self.current_node)
            else:
                # If the visited edge leads to a pickup node, add the passenger and the dropoff node
                self.passengers_on_board.append(self.current_node.dropoff)

        return edge

    def next(self, node: Node) -> Union[Edge, None]:
        # Find the viable edges for the ant in the current situation
        visited_nodes = [edge.from_node for edge in self.route] + [node]
        dropoff_nodes = [node.dropoff for node in visited_nodes if node.dropoff is not None]
        if len(self.passengers_on_board) >= Ant.capacity:
            edges = [edge for node, edge in node.edges[self.num].items() if node in dropoff_nodes]
        else:
            edges = [edge for node, edge in node.edges[self.num].items() if node.dropoff is not None or node in dropoff_nodes]
        edges = filter(lambda e: e.to_node not in visited_nodes, edges)
        edges = filter(lambda e: e.to_node.visited is False, edges)
        edges = list(edges)

        if len(edges) == 0:
            return None

        local_max_cost = max(edge.cost for edge in edges) * (len(self.passengers_on_board) + 1)

        # Calculate the probability distribution of all the viable edges
        edge_points = {}
        for edge in edges:
            pheromones = edge.pheromones
            if len(node.edges) > 1:
                pheromones += (sum(edges.pheromones for edges in [node.edges[i][edge.to_node] for i in range(len(node.edges)) if i != self.num]) / (len(node.edges) - 1))

            delivery_cost_sum = 0
            for dropoff in self.passengers_on_board:
                delivery_cost_sum += edge.to_node.edges[self.num][dropoff].cost if edge.to_node != dropoff else 0

            cost = edge.cost + delivery_cost_sum / Ant.R
            normalized_cost = cost / local_max_cost
            inverse_cost = 10 ** (1 - normalized_cost)
            edge_points[edge] = pheromones * inverse_cost**Ant.b

        # High values of q will force the algorithm to do more exploitation and less exploration
        if random.random() < Ant.q:
            edge, max_points = max(edge_points.items(), key=operator.itemgetter(1))
            return edge

        # Select a random edge based on the distribution calculated above
        number = random.uniform(0, sum(edge_points.values()))
        c = 0
        for edge in edges:
            c += edge_points[edge]
            if c >= number:
                return edge
