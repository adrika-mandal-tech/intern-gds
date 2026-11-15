"""A couple of algorithms written out longhand, so you can see inside them.

networkx has perfectly good implementations of everything here. These exist for
two reasons:

  1. ``pagerank_iters`` returns the **number of rounds** it took as well as the
     answer. networkx does not expose that, and the round count is the whole
     point of Part 1 - it is the thing that depends on the graph's shape rather
     than its size.

  2. Reading a twenty-line implementation of PageRank is a much faster route to
     understanding it than reading a description of PageRank.

``pagerank_iters`` is tested against ``networkx.pagerank`` and agrees with it to
within the convergence tolerance. If you change it, that test should fail.
"""

from __future__ import annotations


def pagerank_iters(G, alpha: float = 0.85, tol: float = 1e-6,
                   max_iter: int = 200):
    """PageRank by power iteration. Returns ``(scores, iterations)``.

    The algorithm, in words: every node starts with an equal share. Each round,
    every node hands its score out equally along its outgoing edges. A node with
    no outgoing edges would leak its score out of the system, so that leaked
    portion is collected and spread evenly over everybody. Finally ``1 - alpha``
    of all the score is taken away and redistributed evenly - the "random jump"
    - which is what guarantees the process settles on a unique answer.

    Stop when no node's score moved by more than ``tol``.

    Raises ``RuntimeError`` if it has not settled within ``max_iter`` rounds,
    rather than quietly returning a half-converged answer.
    """
    nodes = list(G)
    n = len(nodes)
    if n == 0:
        return {}, 0

    if G.is_directed():
        out_degree = {u: G.out_degree(u) for u in nodes}
        incoming = {u: list(G.predecessors(u)) for u in nodes}
    else:
        out_degree = {u: G.degree(u) for u in nodes}
        incoming = {u: list(G.neighbors(u)) for u in nodes}

    dangling = [u for u in nodes if out_degree[u] == 0]
    score = {u: 1.0 / n for u in nodes}

    for iteration in range(1, max_iter + 1):
        leaked = sum(score[u] for u in dangling) / n
        nxt = {}
        for u in nodes:
            total = leaked
            for v in incoming[u]:
                total += score[v] / out_degree[v]
            nxt[u] = alpha * total + (1.0 - alpha) / n

        delta = max(abs(nxt[u] - score[u]) for u in nodes)
        score = nxt
        if delta < tol:
            return score, iteration

    raise RuntimeError(
        "PageRank did not settle within %d rounds (largest change still %.2e). "
        "That is a finding, not a crash - write it down." % (max_iter, delta))
