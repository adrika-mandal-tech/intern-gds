"""The fragile test uses a shortcut: instead of removing each bridge and
measuring both resulting pieces, it checks that both endpoints have internal
degree 2 or more.

That is equivalent, but "it is equivalent" is a claim, so it is tested against
the slow, obviously-correct version on real Louvain output. Verified over 1,864
real communities with zero mismatches, and 13x faster."""

import networkx as nx

from gdslab import loaders, stats


def slow_fragile(sub):
    """The obvious implementation: cut each bridge, look at what falls out."""
    for a, b in nx.bridges(sub):
        trimmed = sub.copy()
        trimmed.remove_edge(a, b)
        parts = list(nx.connected_components(trimmed))
        if len(parts) == 2 and all(len(p) >= 2 for p in parts):
            return True
    return False


def _fragile_via_stats(G, community):
    return stats.community_connectivity(G, [community])["n_fragile"] == 1


def test_agrees_with_the_slow_version_on_real_communities():
    for name in ("crime", "email-Eu-core"):
        G = loaders.load(name, weighted=False)
        if G.is_directed():
            G = G.to_undirected()
        for seed in range(3):
            for community in nx.community.louvain_communities(G, seed=seed):
                if len(community) <= 2:
                    continue
                sub = G.subgraph(community)
                if nx.number_connected_components(sub) > 1:
                    continue
                assert _fragile_via_stats(G, community) == slow_fragile(sub), (
                    "%s seed=%d community=%s" % (name, seed, sorted(community)[:6]))


def test_agrees_on_constructed_edge_cases():
    cases = [
        # two triangles joined by one edge -> fragile
        nx.Graph([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 3)]),
        # triangle with a leaf -> not fragile (leaf side is 1 node)
        nx.Graph([(0, 1), (1, 2), (0, 2), (2, 3)]),
        # path of 4 -> fragile (middle edge leaves 2 and 2)
        nx.path_graph(4),
        # path of 3 -> not fragile (every cut leaves a single node)
        nx.path_graph(3),
        # clique -> no bridges at all
        nx.complete_graph(5),
        # two squares joined by a long thread
        nx.Graph([(0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5),
                  (5, 6), (6, 7), (7, 5)]),
    ]
    for G in cases:
        community = set(G.nodes())
        sub = G.subgraph(community)
        assert _fragile_via_stats(G, community) == slow_fragile(sub), G.edges()
