from ouroboros_graph.ouroboros_graph import OuroborosGraph


def test_delete_node():
    g = OuroborosGraph(directed=True)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)
    g.add_edge(1, 2, -1)
    g.add_edge(1, 3, -1)
    g.add_edge(4, 1, -1)
    g.add_edge(4, 2, -1)
    g.add_edge(3, 2, -1)
    g.delete_node(1)
    assert g.size() == 3
    assert g.nodes() == {2, 3, 4}
    assert g.tuple_edges() == {(4, 2, -1), (3, 2, -1)}
