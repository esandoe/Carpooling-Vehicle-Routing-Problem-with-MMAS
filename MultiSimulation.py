import random

from Ant import Ant
from Graph import *


class Simulation:
    def __init__(self, data: List[Tuple], N: int):
        start_node, nodes, edges = create_graph_from_data(data, N)
        self.start_node = start_node
        self.nodes = nodes
        self.edges = edges
        self.best_solution: List[List[Edge]] = []
        self.best_score = 0
        self.best_solution_cost = 0

        self.max_cost = 0
        for node in nodes:
            node_edges = [edge for node, edge in node.edges[0].items()]
            self.max_cost += max(edge.cost for edge in node_edges)

        self.N = N  # Number of vehicles
        self.reset = 500  # The number of iterations between each time we reset pheromone levels to max
        self.iteration = 0  # iteration counter

    def update(self):
        # Create one ant per vehicle and
        ants = [Ant(self.start_node, ant_num) for ant_num in range(self.N)]
        visited_nodes = [self.start_node]

        # Reset all nodes as not visited
        for node in self.nodes:
            node.visited = False

        # Let the ants free!!!
        max_length = len(self.nodes) + 1
        ant_dist = [1 for _ in range(self.N)]
        while len(visited_nodes) < max_length:
            ant_num = roulette(ant_dist)  # choose the next ant based on how long they have travelled so far
            edge = ants[ant_num].walk()

            # if the ant returns None it has finished, so we just increase the recorded distance by max_cost
            # so that it likely won't be chosen to walk again
            ant_dist[ant_num] += self.max_cost if edge is None else edge.cost

            if edge is not None:
                edge.to_node.visited = True
                visited_nodes.append(edge.to_node)

        # calculate cost and score
        total_cost = sum([ant.total_passenger_time / Ant.R for ant in ants])
        total_score = self.max_cost / float(total_cost)

        # If this is the global best ant, update the best_route with the route
        if total_score > self.best_score:
            self.best_solution = [ant.route for ant in ants]
            self.best_score = total_score
            self.best_solution_cost = total_cost

        for edge in self.edges:
            edge.evaporation()

        # Give pheromones to the global best route
        for i in range(len(self.best_solution)):
            for edge in self.best_solution[i]:
                edge.add_pheromones(total_score)

        self.iteration += 1
        if self.iteration % self.reset == 0:
            self.reset_pheromones()

        return [ant.route for ant in ants]

    def reset_pheromones(self):
        for edge in self.edges:
            edge.pheromones = Edge.max_pheromones


def roulette(values: List[float]):
    # Uncomment the following lines to use an argmax based solution instead of randomness
    # arg_min = min(values)
    # index = values.index(arg_min)
    # return index

    values = [1/value for value in values]
    num = random.uniform(0, sum(values))
    choice = 0
    s = values[0]
    while s < num:
        choice += 1
        s += values[choice]
    return choice
