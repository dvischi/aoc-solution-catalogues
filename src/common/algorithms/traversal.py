"""Collection of common traversal algorithms."""

from queue import PriorityQueue
import numpy as np

def find_shortest_paths(graph, start_node):
    """
    Finds the shortes paths from start_node to any other node.

    It returns a map of predecessors for each node along the shortest path
    as well as a map with the shortest distance between start_node and
    any other node.
    """
    shortest_dists = {}
    predecessors = {}

    for node in graph.get_nodes():
        shortest_dists[node] = np.inf
    shortest_dists[start_node] = 0

    visited_nodes = set()
    unvisited_nodes = PriorityQueue()
    unvisited_nodes.put((0, start_node))

    while not unvisited_nodes.empty():
        # returns the item with the lowest value first
        _, node = unvisited_nodes.get()

        for neighbor in graph.get_neighbours(node):
            distance = (
                shortest_dists[node] +
                graph.get_weight(node, neighbor)
            )

            if distance < shortest_dists[neighbor]:
                shortest_dists[neighbor] = distance
                predecessors[neighbor] = node

                if neighbor not in visited_nodes:
                    # long paths result in a large value (= lowest priority)
                    unvisited_nodes.put((
                        shortest_dists[neighbor],
                        neighbor
                    ))

        visited_nodes.add(node)

    return predecessors, shortest_dists
