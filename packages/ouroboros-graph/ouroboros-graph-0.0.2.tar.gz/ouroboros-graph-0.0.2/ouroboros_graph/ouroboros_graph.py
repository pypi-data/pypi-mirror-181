from typing import Set


class OuroborosGraph:
    """
    An adjacency list implementation of a Graph Abstract Data Type
    """

    class Edge:
        """
        A single edge in an OGraph
        """

        __slots__ = "_start", "_end", "_data"

        def __init__(self, start, end, data):
            self._start = start
            self._end = end
            self._data = data

        def start(self):
            """
            Returns the starting node of the edge
            :return: starting node of the edge
            """
            return self._start

        def end(self):
            """
            Returns ending node of the edge
            :return: ending node of the edge
            """
            return self._end

        def data(self):
            """
            Returns the data of the edge
            :return: data of the edge
            """
            return self._data

        def to_tuple(self):
            """
            Converts to a tuple
            :return: a tuple (start, end, data)
            """
            return self._start, self._end, self._data

        def __hash__(self):
            return hash(id(self))

    def __init__(self, directed=False):
        self._size = 0
        self._num_edges = 0
        self._directed = directed
        self._outgoing = {}
        self._incoming = {}

    def size(self):
        """
        Returns the number of nodes in the graph
        :return: number of nodes in the graph
        """
        return self._size

    def num_edges(self):
        """
        Returns the number of edges in the graph
        :return:
        """
        return self._num_edges

    def is_directed(self) -> bool:
        """
        Returns whether the graph is directed
        :return: True if the graph is directed, false otherwise
        """
        return self._directed

    def contains(self, x) -> bool:
        """
        Returns whether node x exists in the graph
        :param x: The node to test
        :return: True if x is in the graph, false otherwise
        """
        return x in self._outgoing

    def contains_edge(self, x, y):
        """
        Returns whether the edge (x, y) exists
        :param x: starting node of the edge
        :param y: ending node of the edge
        :return: True if the edge exists
        """
        return y in self._outgoing[x]

    def nodes(self) -> Set:
        """
        Returns a set of all the nodes
        :return: A set of all the nodes
        """
        return set(self._outgoing.keys())

    def adjacent_nodes(self, x):
        """
        Returns a set of the adjacent nodes to x, nodes
        which are immediately reachable by x
        :param x:
        :return: returns adjacent nodes
        """
        return set(self._outgoing[x].keys())

    def is_adjacent(self, x, y):
        """
        Returns whether y is adjacent to x, which is True
        if y is immediately reachable by an edge from x
        :param x: the starting node
        :param y: the questioned node
        :return: True if y is adjacent to x, false otherwise
        """
        return y in self.adjacent_nodes(x)

    def edges(self) -> Set[Edge]:
        """
        Returns a set of all the edges
        :return: A set of all the edges
        """
        def find_edges(mapping, result):
            for secondary_dict in mapping.values():
                result.update(secondary_dict.values())
        edges = set()
        find_edges(self._outgoing, edges)
        if self.is_directed():
            find_edges(self._incoming, edges)
        return edges

    def tuple_edges(self):
        edges = self.edges()
        return {edge.to_tuple() for edge in edges}

    def add_node(self, x) -> None:
        """
        Adds the node x to the graph
        :param x: the node to be added
        :return:
        :raises Exception: when node exists already
        """
        if self.contains(x):
            raise Exception("Node exists already.")
        self._size += 1
        self._outgoing[x] = {}
        self._incoming[x] = {}

    def add_edge(self, x, y, value=None):
        """
        Inserts an edge between x and y with data z
        :param x: the starting node of the edge
        :param y: the ending node of the edge
        :param value: data on the node
        :return:
        :raises Exception: when x or y are not nodes in the graph, or if edge exists
        """
        if not self.contains(x) or not self.contains(y):
            raise Exception("Cannot insert edge with missing node.")
        if self.contains_edge(x, y):
            raise Exception("Cannot insert edge that already exists.")
        self._num_edges += 1
        edge = self.Edge(x, y, value)
        self._outgoing[x][y] = edge
        self._incoming[y][x] = edge
        if not self.is_directed():
            edge2 = self.Edge(y, x, value)
            self._outgoing[y][x] = edge2
            self._incoming[x][y] = edge2

    def delete_node(self, x):
        """
        Deletes the node from the graph and its associated edges
        :param x: the node to be deleted
        :return:
        :raises Exception: when x is not in the graph
        """
        if not self.contains(x):
            raise Exception("Cannot delete node that does not exist.")
        for y in self._outgoing[x]:
            del self._incoming[y][x]
        del self._outgoing[x]
        for y in self._incoming[x]:
            del self._outgoing[y][x]
        del self._incoming[x]
        self._size -= 1

    def delete_edge(self, x, y):
        """
        Deletes the edge from x to y. If graph is undirected, then
        deletes the undirected edge
        :param x: the starting node
        :param y: the ending node
        :return:
        :raises Exception: when nodes are missing or edge does not exist
        """
        if not self.contains(x) or not self.contains(y):
            raise Exception("Cannot delete edge with missing node.")
        if not self.is_adjacent(x, y):
            raise Exception("Edge does not exist.")
        del self._outgoing[x][y]
        del self._incoming[y][x]
        if not self.is_directed():
            del self._outgoing[y][x]
            del self._incoming[x][y]
        self._num_edges -= 1

    def clear(self):
        self._outgoing = {}
        self._incoming = {}
        self._num_edges = 0
        self._size = 0

    def overwrite_graph(self, edge_list=[]):
        """
        Takes in a list of tuples (x, y, value) and overwrites the existing graph
        :param edge_list: list of edges to generate the new connected graph
        :return:
        """
        self.clear()
        for x, y, value in edge_list:
            if not self.contains(x):
                self.add_node(x)
            if not self.contains(y):
                self.add_node(y)
            if not self.contains_edge(x, y):
                self.add_edge(x, y, value)
