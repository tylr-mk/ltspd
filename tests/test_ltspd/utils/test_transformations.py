from ltspd.utils.transformations import pairings_to_graph, subgraphing_groups


def test_pairings_to_graph_explodes_groups():
    graph = pairings_to_graph([(0, 1, 2), (3, 4)])
    assert graph.has_edge(0, 2)
    assert graph.has_edge(3, 4)
    assert not graph.has_edge(2, 3)
    assert graph.number_of_edges() == 4


def test_pairings_to_graph_pairs_as_is():
    graph = pairings_to_graph([(0, 1), (1, 2)], explode=False)
    assert sorted(graph.edges) == [(0, 1), (1, 2)]


def test_subgraphing_groups():
    graph = subgraphing_groups([(0, 1), (2, 3, 4)], max_steps=None)
    hubs = [n for n in graph.nodes if str(n).startswith("SUBGROUP_")]
    assert len(hubs) == 2
    assert sorted(len(graph[h]) for h in hubs) == [2, 3]
