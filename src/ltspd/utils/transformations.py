"""Key object transformations between object types for analysis and functions

The library offers ways to plan, generate, and evaluate events and activities
through some key methods. Current scope are single non-directed graphs.
"""

from itertools import product

from networkx import Graph

from ltspd.utils import random_string
from ltspd.utils.groups import explode_subgroups


def pairings_to_graph(pairings, explode=True, graph=None):
    """Add an edge between every pair of members that share a group. With
    explode=False pairings must already be 2-tuples and are added as-is.
    """
    graph = graph if graph else Graph()
    graph.add_edges_from(explode_subgroups(pairings, 2) if explode else pairings)
    return graph


def subgraphing_groups(groups, max_steps):
    """Place a grouped set of participants into graphs with connections drawn
    only between members of each group"""
    graph = Graph()
    for g in groups:
        subgroup_node = f"SUBGROUP_{random_string()}"
        graph.add_node(subgroup_node)
        graph.add_edges_from(product((subgroup_node,), g))
    return graph
