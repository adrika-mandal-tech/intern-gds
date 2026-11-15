"""Describe a graph's shape.

The point of this module is one number: ``degree_skew``.

Two graphs can have almost the same node count and edge count and still behave
completely differently, because what actually drives the cost of most graph
algorithms is how *unevenly* the connections are spread. A graph where every
node has four neighbours and a graph where one node has four thousand are not
the same problem, and no amount of counting nodes will tell you which you have.

``degree_skew`` is ``degree_max / degree_median`` - how many times more
connected the busiest node is than the typical one. It is deliberately crude.
You will be asked in Part 1 whether it predicts cost better than node count
does; find out rather than take our word for it.
"""

from __future__ import annotations

import statistics

import networkx as nx

FIELDS = [
    "name", "nodes", "edges", "density",
    "degree_min", "degree_median", "degree_mean", "degree_max", "degree_skew",
    "components", "largest_component_frac", "clustering",
    "is_directed", "is_weighted",
]


def profile_graph(G, name: str) -> dict:
    """Return the shape of ``G`` as a flat dict with keys :data:`FIELDS`.

    For a directed graph, degree means total degree (in plus out), and
    components means weakly connected components.
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    degrees = [d for _, d in G.degree()]

    if G.is_directed():
        comps = list(nx.weakly_connected_components(G))
        clustering = nx.average_clustering(G.to_undirected())
    else:
        comps = list(nx.connected_components(G))
        clustering = nx.average_clustering(G)

    median = statistics.median(degrees) if degrees else 0
    largest = max((len(c) for c in comps), default=0)
    weighted = any("weight" in d for _, _, d in G.edges(data=True))

    return {
        "name": name,
        "nodes": n,
        "edges": m,
        "density": nx.density(G),
        "degree_min": min(degrees) if degrees else 0,
        "degree_median": median,
        "degree_mean": (sum(degrees) / len(degrees)) if degrees else 0.0,
        "degree_max": max(degrees) if degrees else 0,
        "degree_skew": (max(degrees) / max(median, 1)) if degrees else 0.0,
        "components": len(comps),
        "largest_component_frac": (largest / n) if n else 0.0,
        "clustering": clustering,
        "is_directed": G.is_directed(),
        "is_weighted": weighted,
    }
