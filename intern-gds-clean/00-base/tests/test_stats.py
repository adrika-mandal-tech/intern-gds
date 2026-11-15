import networkx as nx
import pytest

from gdslab import stats


def test_identical_partitions_score_one():
    a = {"x": 0, "y": 0, "z": 1}
    assert stats.adjusted_rand(a, dict(a)) == pytest.approx(1.0)
    assert stats.nmi(a, dict(a)) == pytest.approx(1.0)


def test_relabelling_does_not_change_the_score():
    a = {"x": 0, "y": 0, "z": 1}
    b = {"x": 7, "y": 7, "z": 3}
    assert stats.adjusted_rand(a, b) == pytest.approx(1.0)
    assert stats.nmi(a, b) == pytest.approx(1.0)


def test_everything_in_one_group_scores_about_zero():
    a = {"a": 0, "b": 0, "c": 1, "d": 1}
    b = {"a": 0, "b": 0, "c": 0, "d": 0}
    assert abs(stats.adjusted_rand(a, b)) < 1e-9


def test_partition_hash_ignores_label_and_order():
    assert stats.partition_hash([{"a", "b"}, {"c"}]) == \
           stats.partition_hash([{"c"}, {"b", "a"}])


def test_partition_hash_separates_different_partitions():
    assert stats.partition_hash([{"a", "b"}, {"c"}]) != \
           stats.partition_hash([{"a"}, {"b", "c"}])


def test_top_k_overlap():
    a = {"a": 9, "b": 8, "c": 7, "d": 1}
    b = {"a": 9, "b": 8, "c": 0, "d": 7}
    assert stats.top_k_overlap(a, b, 2) == pytest.approx(1.0)
    assert stats.top_k_overlap(a, b, 3) == pytest.approx(0.5)  # {a,b,c} vs {a,b,d}


def test_spearman_of_identical_rankings_is_one():
    a = {"a": 1, "b": 2, "c": 3}
    assert stats.spearman(a, dict(a)) == pytest.approx(1.0)


def test_spearman_of_reversed_rankings_is_minus_one():
    a = {"a": 1, "b": 2, "c": 3}
    b = {"a": 3, "b": 2, "c": 1}
    assert stats.spearman(a, b) == pytest.approx(-1.0)


def test_connectivity_flags_a_deliberately_split_community():
    # two triangles with no edge between them, declared as ONE community
    G = nx.disjoint_union(nx.complete_graph(3), nx.complete_graph(3))
    out = stats.community_connectivity(G, [set(G.nodes())])
    assert out["n_communities"] == 1
    assert out["n_disconnected"] == 1
    assert out["frac_disconnected"] == pytest.approx(1.0)


def test_connectivity_passes_genuinely_connected_communities():
    G = nx.disjoint_union(nx.complete_graph(3), nx.complete_graph(3))
    out = stats.community_connectivity(G, [{0, 1, 2}, {3, 4, 5}])
    assert out["n_disconnected"] == 0
    assert out["frac_disconnected"] == pytest.approx(0.0)


def test_fragile_flags_two_clumps_joined_by_one_edge():
    """Two triangles joined by a single edge: connected, but cutting that edge
    leaves two substantial pieces. This is the discriminating case."""
    G = nx.Graph([(0, 1), (1, 2), (0, 2),      # triangle A
                  (3, 4), (4, 5), (3, 5),      # triangle B
                  (2, 3)])                     # the thread
    out = stats.community_connectivity(G, [set(G.nodes())])
    assert out["n_disconnected"] == 0
    assert out["n_fragile"] == 1
    assert out["n_pendant"] == 0


def test_a_leaf_is_pendant_not_fragile():
    """A triangle plus one dangling node. Real, but ordinary - it must NOT be
    counted as fragile, or the metric stops discriminating."""
    G = nx.Graph([(0, 1), (1, 2), (0, 2), (2, 3)])
    out = stats.community_connectivity(G, [{0, 1, 2, 3}])
    assert out["n_disconnected"] == 0
    assert out["n_fragile"] == 0
    assert out["n_pendant"] == 1


def test_a_clique_is_none_of_the_three():
    G = nx.complete_graph(5)
    out = stats.community_connectivity(G, [set(G.nodes())])
    assert out["n_disconnected"] == 0
    assert out["n_fragile"] == 0
    assert out["n_pendant"] == 0


def test_small_communities_are_excluded_from_the_denominator():
    """Singletons cannot be disconnected, fragile or pendant. Counting them in
    the denominator would dilute every rate with communities that were never
    eligible to fail."""
    G = nx.Graph([(0, 1)])
    out = stats.community_connectivity(G, [{0}, {1}])
    assert out["n_communities"] == 2   # they existed
    assert out["n_assessed"] == 0      # but none could be judged
    assert out["n_disconnected"] == 0
    assert out["n_fragile"] == 0
    assert out["n_pendant"] == 0


def test_rates_are_over_assessed_not_over_total():
    """One real fragile community plus 9 singletons is a 100% rate, not 10%."""
    G = nx.Graph([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 3)])
    for i in range(10, 19):
        G.add_node(i)
    communities = [set(range(6))] + [{i} for i in range(10, 19)]
    out = stats.community_connectivity(G, communities)
    assert out["n_communities"] == 10
    assert out["n_assessed"] == 1
    assert out["frac_fragile"] == pytest.approx(1.0)


def test_categories_are_mutually_exclusive():
    """A community is counted once, most-serious first."""
    G = nx.Graph([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 3), (5, 6)])
    out = stats.community_connectivity(G, [set(G.nodes())])
    assert out["n_disconnected"] + out["n_fragile"] + out["n_pendant"] == 1
    assert out["n_fragile"] == 1  # fragile outranks the pendant node 6


def test_the_metric_can_actually_return_zero_and_one():
    """A metric that cannot vary is not measuring anything. Prove both ends."""
    clique = nx.complete_graph(6)
    assert stats.community_connectivity(
        clique, [set(clique.nodes())])["frac_fragile"] == 0.0
    barbell = nx.Graph([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 3)])
    assert stats.community_connectivity(
        barbell, [set(barbell.nodes())])["frac_fragile"] == 1.0


def test_modularity_prefers_the_natural_split():
    G = nx.disjoint_union(nx.complete_graph(4), nx.complete_graph(4))
    G.add_edge(0, 4)
    good = stats.modularity(G, [{0, 1, 2, 3}, {4, 5, 6, 7}])
    lumped = stats.modularity(G, [set(G.nodes())])
    assert good > lumped
    assert abs(lumped) < 1e-9
