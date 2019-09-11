"""Key object transformations between object types for analysis and functions

The library offers ways to plan, generate, and evaluate events and activities
through some key methods. Current scope are single non-directed graphs.
"""

from itertools import product

from ltspd.utils import explode_subgroups, random_string
from networkx import Graph


def pairings_to_graph(pairings, explode=False, G=None):
    G = G if G else Graph()
    if explode:
        G.add_edges_from(pairings)
    else:
        G.add_edges_from(explode_subgroups(pairings, 2))
    return G


def subgraphing_groups(groups, max_steps):
    """Place a grouped set of participants into graphs with connections drawn
    only between members of each group"""
    G = Graph()
    for g in groups:
        subgroup_node = "SUBGROUP_{}".format(random_string())
        G.add_node(subgroup_node)
        G.add_edges_from(product((subgroup_node,), g))
    return G
