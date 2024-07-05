"""Collection of common data structures."""

import abc

class Graph(metaclass=abc.ABCMeta):
    """Abstract class representing a graph."""
    @abc.abstractmethod
    def get_nodes(self):
        """Get all nodes of the graph."""

    @abc.abstractmethod
    def get_neighbours(self, node):
        """Get all neighbours of a node."""

    @abc.abstractmethod
    def get_weight(self, src_node, dest_node):
        """Get the weight of the edge connecting src_node with dest_node."""
