"""Graphs where you already know the right answer.

Every graph in this folder is real, which makes it honest and makes it useless
for one specific purpose: you cannot tell whether an algorithm got the *correct*
answer, only whether two algorithms agree with each other. Agreement is not
correctness. Two algorithms can agree and both be wrong.

These generators build graphs with the answer planted in them. If you ask a
community-detection algorithm to find the groups in a planted-partition graph,
you can score it, because you put the groups there.

Everything is generated from a fixed seed, so your graphs and your colleague's
are identical.

    from make_synthetic import bridge_graph, planted_partition, lfr

Or run it directly to see them described:

    python 03-data/make_synthetic.py
"""

from __future__ import annotations

import networkx as nx


def bridge_graph():
    """Two tight groups of four, joined by exactly one edge.

    Returns ``(G, truth)`` where ``truth`` maps each node to its group.

    The smallest graph that makes the point of this whole field. Nodes C and E
    sit on the only route between the halves. Count each node's connections and
    C looks about a third better connected than the rest - a difference you
    would dismiss. Measure how much traffic must pass through each node and C
    carries every single route between the halves while six of the eight carry
    none.

    Same graph. One measure shrugs; the other finds the thing that would break
    the network if you removed it.
    """
    G = nx.Graph()
    left = ["A", "B", "C", "D"]
    right = ["E", "F", "G", "H"]
    for group in (left, right):
        for i, u in enumerate(group):
            for v in group[i + 1:]:
                G.add_edge(u, v)
    G.add_edge("C", "E")  # the only bridge
    truth = {n: 0 for n in left}
    truth.update({n: 1 for n in right})
    return G, truth


def planted_partition(groups: int = 8, per_group: int = 40,
                      p_in: float = 0.35, p_out: float = 0.01, seed: int = 7):
    """``groups`` clumps of ``per_group`` nodes, densely wired inside, sparsely between.

    Returns ``(G, truth)``. The groups are planted, so a community-detection
    algorithm's answer can be scored against ``truth`` with ARI or NMI.

    Raise ``p_out`` towards ``p_in`` and the groups blur together. That is a
    knob worth turning: it tells you the point at which the structure stops
    being findable, which is a far more useful thing to know about an algorithm
    than whether it works on an easy case.
    """
    G = nx.planted_partition_graph(groups, per_group, p_in, p_out, seed=seed)
    truth = {n: n // per_group for n in G.nodes()}
    return G, truth


def lfr(n: int = 500, tau1: float = 2.5, tau2: float = 1.5, mu: float = 0.15,
        average_degree: float = 10, min_community: int = 25, seed: int = 7):
    """An LFR benchmark graph - the standard test for community detection.

    Returns ``(G, truth)``.

    More realistic than planted partition: node degrees and community sizes are
    both drawn from power laws, like real networks. ``mu`` is the mixing
    parameter - the fraction of each node's edges that go outside its own
    community. Low mu is easy, high mu is hard, and somewhere around 0.5 the
    community structure stops being recoverable even in principle.

    Generation is iterative and can fail to converge for awkward parameter
    combinations; it raises ``networkx.ExceededMaxIterations`` when it does.
    That is not your fault - change the parameters.
    """
    G = nx.LFR_benchmark_graph(n=n, tau1=tau1, tau2=tau2, mu=mu,
                               average_degree=average_degree,
                               min_community=min_community, seed=seed)
    G.remove_edges_from(nx.selfloop_edges(G))
    truth = {}
    for node, data in G.nodes(data=True):
        truth[node] = min(data["community"])  # canonical id for the community
    return nx.Graph(G), truth


SYNTHETIC = {
    "bridge": bridge_graph,
    "planted": planted_partition,
    "lfr": lfr,
}


def main():
    from gdslab import profile, stats
    print("%-10s %6s %7s %7s %6s  %s" % ("name", "N", "E", "groups", "skew", "note"))
    print("-" * 78)
    for name, builder in SYNTHETIC.items():
        G, truth = builder()
        p = profile.profile_graph(G, name)
        communities = {}
        for node, group in truth.items():
            communities.setdefault(group, set()).add(node)
        q = stats.modularity(G, list(communities.values()))
        print("%-10s %6d %7d %7d %6.1f  true-grouping modularity = %+.4f"
              % (name, p["nodes"], p["edges"], len(communities),
                 p["degree_skew"], q))
    print("\nEach of these carries its own correct answer. Use them to find out")
    print("whether an algorithm is right - not merely whether two agree.")


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
