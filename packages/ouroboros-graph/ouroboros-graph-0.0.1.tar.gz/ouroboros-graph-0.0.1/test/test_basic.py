import pytest
from ouroboros_graph.ouroboros_graph import OuroborosGraph


def test_is_directed():
    g1 = OuroborosGraph(directed=True)
    g2 = OuroborosGraph()
    assert g1.is_directed()
    assert not g2.is_directed()


def test_size():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.delete_node(3)
    assert g.size() == 2


def test_num_edges():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1, 2, -1)
    g.add_edge(2, 3, -1)
    g.delete_edge(2, 3)
    assert g.num_edges() == 1


def test_contains():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    assert g.contains(1)
    assert g.contains(2)
    assert g.contains(3)
    assert not g.contains(4)


def test_contains_edge():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1, 2, -1)
    g.add_edge(2, 3, -1)
    assert g.contains_edge(1, 2)
    assert g.contains_edge(2, 3)
    assert not g.contains_edge(3, 1)


def test_nodes():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    assert g.nodes() == {1, 2, 3}


def test_edges():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1, 2, -1)
    g.add_edge(2, 3, -1)
    g.add_edge(3, 1, None)
    expected = {(1, 2, -1), (2, 3, -1), (3, 1, None),
                (2, 1, -1), (3, 2, -1), (1, 3, None)}
    edges = {e.to_tuple() for e in g.edges()}
    assert expected == edges


def test_tuple_edges():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1, 2, -1)
    g.add_edge(2, 3, -1)
    g.add_edge(3, 1, None)
    assert g.tuple_edges() == {(1, 2, -1), (2, 3, -1), (3, 1, None),
                               (2, 1, -1), (3, 2, -1), (1, 3, None)}


def test_adjacent_nodes():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1, 2, -1)
    g.add_edge(2, 3, -1)
    g.add_edge(1, 3, None)
    assert g.adjacent_nodes(1) == {2, 3}


def test_is_adjacent():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1, 2, -1)
    g.add_edge(2, 3, -1)
    assert g.is_adjacent(1, 2)
    assert g.is_adjacent(2, 1)
    assert g.is_adjacent(2, 3)
    assert g.is_adjacent(3, 2)
    assert not g.is_adjacent(1, 3)


def test_add_node():
    g = OuroborosGraph()
    assert g.size() == 0
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    assert g.size() == 3
    assert g.nodes() == {1, 2, 3}


def test_add_node__already_exists():
    with pytest.raises(Exception, match="Node exists already."):
        g = OuroborosGraph()
        g.add_node(1)
        g.add_node(1)
    assert g.size() == 1


def test_add_edge():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)
    g.add_edge(1, 2, -1)
    g.add_edge(2, 3, -1)
    g.add_edge(3, 1, None)
    assert g.tuple_edges() == {(1, 2, -1), (2, 3, -1), (3, 1, None),
                               (2, 1, -1), (3, 2, -1), (1, 3, None)}
    assert g.num_edges() == 3


def test_add_edge__node_does_not_exist():
    with pytest.raises(Exception, match="Cannot insert edge with missing node."):
        g = OuroborosGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(2, 3, -1)
    assert g.num_edges() == 0


def test_add_edge__edge_exists():
    with pytest.raises(Exception, match="Cannot insert edge that already exists."):
        g = OuroborosGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(1, 2, -1)
        g.add_edge(1, 2, 4)
    assert g.num_edges() == 1


def test_delete_node():
    g = OuroborosGraph()
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
    assert g.tuple_edges() == {(4, 2, -1), (3, 2, -1),
                               (2, 4, -1), (2, 3, -1)}


def test_delete_node__does_not_exist():
    with pytest.raises(Exception, match="Cannot delete node that does not exist."):
        g = OuroborosGraph()
        g.add_node(1)
        g.add_node(2)
        g.delete_node(3)
    assert g.size() == 2


def test_delete_edge():
    g = OuroborosGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)
    g.add_edge(1, 2, -1)
    g.add_edge(2, 3, -1)
    g.add_edge(3, 1, None)
    g.add_edge(2, 4, -1)
    g.delete_edge(2, 3)
    assert g.tuple_edges() == {(1, 2, -1), (3, 1, None), (2, 4, -1),
                               (2, 1, -1), (1, 3, None), (4, 2, -1)}
    assert g.size() == 4
    assert g.num_edges() == 3


def test_delete_edge__does_not_exist():
    with pytest.raises(Exception, match="Cannot delete edge with missing node."):
        g = OuroborosGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_edge(1, 2, -1)
        g.delete_edge(2, 3)
    assert g.num_edges() == 1


def test_delete_edge__node_does_not_exist():
    with pytest.raises(Exception, match="Edge does not exist."):
        g = OuroborosGraph()
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_edge(1, 2, -1)
        g.add_edge(2, 3, -1)
        g.delete_edge(1, 3)
    assert g.num_edges() == 2

