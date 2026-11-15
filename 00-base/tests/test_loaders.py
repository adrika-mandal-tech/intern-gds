import pytest

from gdslab import loaders

EXPECTED = {
    "lesmis": (77, 254),
    "unicodelang": (868, 1255),
    "crime": (1380, 1476),
    "email-Eu-core": (986, 24929),
    "openflights": (3214, 36906),
    "facebook_combined": (4039, 88234),
    "ca-GrQc": (5241, 14484),
}


def test_every_graph_loads_at_the_documented_size():
    for name, (n, m) in EXPECTED.items():
        G = loaders.load(name)
        assert (G.number_of_nodes(), G.number_of_edges()) == (n, m), name


def test_list_graphs_returns_all_seven():
    assert sorted(loaders.list_graphs()) == sorted(EXPECTED)


def test_checksums_all_match():
    assert loaders.verify_checksums() == []


def test_openflights_carries_real_weights():
    G = loaders.load("openflights")
    w = [d["weight"] for _, _, d in G.edges(data=True)]
    assert len(w) == G.number_of_edges()
    assert min(w) > 0
    assert max(w) > 1000  # kilometres, genuinely varying


def test_unweighted_graph_has_no_weight_attribute():
    G = loaders.load("crime")
    assert all("weight" not in d for _, _, d in G.edges(data=True))


def test_weights_can_be_switched_off():
    G = loaders.load("openflights", weighted=False)
    assert all("weight" not in d for _, _, d in G.edges(data=True))


def test_directedness_comes_from_the_manifest():
    assert loaders.load("openflights").is_directed()
    assert not loaders.load("crime").is_directed()


def test_directedness_can_be_overridden():
    G = loaders.load("openflights", directed=False)
    assert not G.is_directed()
    assert G.number_of_edges() == 18858  # reciprocal routes collapse


def test_crime_sides_partition_the_graph():
    G, sd = loaders.load("crime"), loaders.sides("crime")
    assert set(sd) == set(G.nodes())
    assert sorted(set(sd.values())) == [0, 1]
    # a bipartite graph has no edge inside a side
    assert not any(sd[a] == sd[b] for a, b in G.edges())


def test_unicodelang_sides_partition_the_graph():
    G, sd = loaders.load("unicodelang"), loaders.sides("unicodelang")
    assert set(sd) == set(G.nodes())
    assert not any(sd[a] == sd[b] for a, b in G.edges())


def test_sides_on_a_non_bipartite_graph_raises():
    with pytest.raises(KeyError):
        loaders.sides("lesmis")


def test_ground_truth_has_42_departments():
    gt = loaders.ground_truth("email-Eu-core")
    assert len(set(gt.values())) == 42


def test_graph_without_ground_truth_raises():
    with pytest.raises(KeyError):
        loaders.ground_truth("lesmis")


def test_lesmis_has_readable_names():
    nm = loaders.names("lesmis")
    assert len(nm) == 77
    assert nm["11"] == "Valjean"


def test_names_are_not_ground_truth():
    """Node names must not be mistaken for community labels - only one graph in
    the pack has ground-truth communities, and lesmis is not it."""
    with pytest.raises(KeyError):
        loaders.ground_truth("lesmis")
    assert loaders.names("lesmis")  # but it does have names


def test_graph_without_names_raises():
    with pytest.raises(KeyError):
        loaders.names("crime")


def test_the_most_connected_lesmis_character_is_the_protagonist():
    G, nm = loaders.load("lesmis"), loaders.names("lesmis")
    top = max(G.degree(), key=lambda kv: kv[1])
    assert nm[top[0]] == "Valjean"
    assert top[1] == 36


def test_igraph_matches_networkx_size():
    for name in ("crime", "lesmis", "email-Eu-core"):
        g = loaders.load_igraph(name)
        U = loaders.load(name)
        if U.is_directed():
            U = U.to_undirected()
        assert g.vcount() == U.number_of_nodes(), name
        assert g.ecount() == U.number_of_edges(), name


def test_unknown_graph_raises():
    with pytest.raises(KeyError):
        loaders.load("no-such-graph")
