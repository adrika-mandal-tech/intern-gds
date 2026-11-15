import networkx as nx

from gdslab import loaders, profile


def test_star_graph_has_extreme_skew():
    p = profile.profile_graph(nx.star_graph(100), "star")
    assert p["nodes"] == 101 and p["edges"] == 100
    assert p["degree_max"] == 100 and p["degree_median"] == 1
    assert p["degree_skew"] == 100


def test_ring_graph_has_no_skew():
    p = profile.profile_graph(nx.cycle_graph(50), "ring")
    assert p["degree_max"] == p["degree_median"] == 2
    assert p["degree_skew"] == 1
    assert p["components"] == 1


def test_disconnected_graph_reports_components():
    G = nx.disjoint_union(nx.complete_graph(5), nx.complete_graph(3))
    p = profile.profile_graph(G, "two")
    assert p["components"] == 2
    assert abs(p["largest_component_frac"] - 5 / 8) < 1e-9


def test_complete_graph_has_density_one():
    p = profile.profile_graph(nx.complete_graph(6), "k6")
    assert abs(p["density"] - 1.0) < 1e-9
    assert abs(p["clustering"] - 1.0) < 1e-9


def test_directed_graph_is_flagged_and_still_profiles():
    p = profile.profile_graph(loaders.load("openflights"), "openflights")
    assert p["is_directed"] is True
    assert p["is_weighted"] is True
    assert p["nodes"] == 3214


def test_every_shipped_graph_profiles_without_error():
    for name in loaders.list_graphs():
        p = profile.profile_graph(loaders.load(name), name)
        assert p["nodes"] > 0 and p["edges"] > 0
        assert p["degree_skew"] >= 1


def test_field_order_is_stable():
    a = profile.profile_graph(nx.cycle_graph(5), "a")
    b = profile.profile_graph(nx.star_graph(5), "b")
    assert list(a) == list(b) == profile.FIELDS
