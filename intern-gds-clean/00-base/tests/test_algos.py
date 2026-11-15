import networkx as nx
import pytest

from gdslab import algos, loaders


def _max_diff(a, b):
    return max(abs(a[k] - b[k]) for k in a)


def test_matches_networkx_on_a_small_directed_graph():
    G = nx.DiGraph([("A", "B"), ("B", "C"), ("C", "A"), ("C", "D")])
    mine, iters = algos.pagerank_iters(G, tol=1e-10)
    theirs = nx.pagerank(G, tol=1e-12)
    assert _max_diff(mine, theirs) < 1e-6
    assert iters > 0


def test_matches_networkx_on_real_graphs():
    """networkx stops on the L1 norm scaled by N; this one stops on the largest
    single change. The tolerances are therefore not comparable - so both are run
    tight, with enough headroom on max_iter, and the ANSWERS are compared."""
    for name in ("lesmis", "crime", "email-Eu-core"):
        G = loaders.load(name, weighted=False)
        mine, _ = algos.pagerank_iters(G, tol=1e-12, max_iter=2000)
        theirs = nx.pagerank(G, tol=1e-12, max_iter=2000)
        assert _max_diff(mine, theirs) < 1e-6, name


def test_scores_sum_to_one():
    G = loaders.load("crime")
    scores, _ = algos.pagerank_iters(G)
    assert abs(sum(scores.values()) - 1.0) < 1e-6


def test_dangling_nodes_do_not_leak_score():
    # D has no outgoing edges; without redistribution the total would shrink
    G = nx.DiGraph([("A", "B"), ("B", "C"), ("C", "A"), ("C", "D")])
    scores, _ = algos.pagerank_iters(G, tol=1e-10)
    assert abs(sum(scores.values()) - 1.0) < 1e-6


def test_the_bridge_feeding_node_outranks_the_dead_end():
    G = nx.DiGraph([("A", "B"), ("B", "C"), ("C", "A"), ("C", "D")])
    scores, _ = algos.pagerank_iters(G, tol=1e-10)
    # every node has exactly one incoming edge, so degree cannot separate them
    assert len({G.in_degree(n) for n in G}) == 1
    # but PageRank can
    assert scores["C"] > scores["B"] > scores["A"]
    assert scores["A"] == pytest.approx(scores["D"], abs=1e-9)


def test_is_deterministic():
    G = loaders.load("crime")
    a, ia = algos.pagerank_iters(G)
    b, ib = algos.pagerank_iters(G)
    assert ia == ib
    assert a == b


def test_tighter_tolerance_needs_more_rounds():
    G = loaders.load("crime")
    _, loose = algos.pagerank_iters(G, tol=1e-4)
    _, tight = algos.pagerank_iters(G, tol=1e-8)
    assert tight > loose


def test_raises_rather_than_returning_a_half_converged_answer():
    G = loaders.load("email-Eu-core")
    with pytest.raises(RuntimeError):
        algos.pagerank_iters(G, tol=1e-12, max_iter=2)
