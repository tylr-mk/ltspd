"""Key object transformations between object types for analysis and functions

The library offers ways to plan, generate, and evaluate events and activities
through some key methods. Current scope are single non-directed graphs.
"""

from itertools import product

from ltspd.utils import explode_subgroups, random_string
from networkx import Graph


def pairings_to_graph(pairings, explode=False, graph=None):
    graph = graph if graph else Graph()
    if explode:
        graph.add_edges_from(pairings)
    else:
        graph.add_edges_from(explode_subgroups(pairings, 2))
    return graph


def subgraphing_groups(groups, max_steps):
    """Place a grouped set of participants into graphs with connections drawn
    only between members of each group"""
    graph = Graph()
    for g in groups:
        subgroup_node = "SUBGROUP_{}".format(random_string())
        graph.add_node(subgroup_node)
        graph.add_edges_from(product((subgroup_node,), g))
    return graph
