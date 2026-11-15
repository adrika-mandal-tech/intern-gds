"""Ways of comparing two results.

You will constantly need to answer "are these two answers the same?" and the
honest answer is usually "not exactly, and that might be fine". Two runs of a
community-detection algorithm can produce different groupings that are equally
good. Two centrality measures can rank the same graph completely differently and
both be correct, because they are answering different questions.

So: never compare results by equality. Compare them with one of these, and
report the number.

    adjusted_rand / nmi     how much do two groupings agree? (1.0 = identical)
    spearman                how much do two rankings agree? (1.0 = identical)
    top_k_overlap           do two rankings pick the same top few?
    partition_hash          are two groupings byte-identical? (for counting
                            distinct outcomes, not for judging quality)
    modularity              how good is this grouping, on its own terms?
    community_connectivity  do these communities actually hold together?
"""

from __future__ import annotations

import hashlib
import math

import networkx as nx


def _aligned(a: dict, b: dict):
    """Values of two dicts over their shared keys, in a stable order."""
    keys = sorted(set(a) & set(b))
    if not keys:
        raise ValueError("the two inputs share no keys")
    return keys, [a[k] for k in keys], [b[k] for k in keys]


def _contingency(labels_a, labels_b) -> dict:
    table = {}
    for x, y in zip(labels_a, labels_b):
        table[(x, y)] = table.get((x, y), 0) + 1
    return table


def _comb2(n: int) -> float:
    return n * (n - 1) / 2.0


def adjusted_rand(a: dict, b: dict) -> float:
    """Adjusted Rand Index between two groupings. 1.0 identical, ~0.0 chance.

    Insensitive to what the groups are *called* - only to which items are put
    together. That is what you want: an algorithm that finds the same groups but
    numbers them differently has not changed its answer.
    """
    _, la, lb = _aligned(a, b)
    n = len(la)
    table = _contingency(la, lb)
    rows, cols = {}, {}
    for (x, y), count in table.items():
        rows[x] = rows.get(x, 0) + count
        cols[y] = cols.get(y, 0) + count

    sum_ij = sum(_comb2(c) for c in table.values())
    sum_i = sum(_comb2(c) for c in rows.values())
    sum_j = sum(_comb2(c) for c in cols.values())
    total = _comb2(n)
    if total == 0:
        return 1.0
    expected = sum_i * sum_j / total
    maximum = (sum_i + sum_j) / 2.0
    if maximum == expected:
        return 1.0
    return (sum_ij - expected) / (maximum - expected)


def nmi(a: dict, b: dict) -> float:
    """Normalised Mutual Information between two groupings. 1.0 identical."""
    _, la, lb = _aligned(a, b)
    n = len(la)
    table = _contingency(la, lb)
    rows, cols = {}, {}
    for (x, y), count in table.items():
        rows[x] = rows.get(x, 0) + count
        cols[y] = cols.get(y, 0) + count

    def entropy(counts):
        return -sum((c / n) * math.log(c / n) for c in counts.values() if c > 0)

    h_a, h_b = entropy(rows), entropy(cols)
    mutual = 0.0
    for (x, y), count in table.items():
        if count:
            mutual += (count / n) * math.log((count / n) / ((rows[x] / n) * (cols[y] / n)))
    if h_a == 0 and h_b == 0:
        return 1.0
    denominator = (h_a + h_b) / 2.0
    return mutual / denominator if denominator > 0 else 0.0


def spearman(a: dict, b: dict) -> float:
    """Spearman rank correlation between two score dicts. +1 agree, -1 opposite."""
    from scipy.stats import spearmanr
    _, va, vb = _aligned(a, b)
    value = spearmanr(va, vb).statistic
    return float(value) if value == value else 0.0  # NaN when a side is constant


def top_k_overlap(a: dict, b: dict, k: int) -> float:
    """Jaccard overlap of the top-``k`` keys of two score dicts.

    Ties are broken by key so the result is reproducible. If you care about the
    ties themselves, look at the scores - this deliberately hides them.
    """
    def top(scores):
        return {key for key, _ in sorted(scores.items(),
                                         key=lambda kv: (-kv[1], str(kv[0])))[:k]}
    sa, sb = top(a), top(b)
    union = sa | sb
    return len(sa & sb) / len(union) if union else 1.0


def partition_hash(communities) -> str:
    """A stable fingerprint of a grouping, ignoring order and group labels.

    Use this to *count distinct outcomes* across many runs. Do not use it to
    decide whether one grouping is better than another - a different hash means
    different, not worse.
    """
    canonical = sorted(tuple(sorted(map(str, community))) for community in communities)
    return hashlib.sha256(repr(canonical).encode("utf-8")).hexdigest()[:16]


def modularity(G, communities) -> float:
    """How much better connected these groups are than chance would give."""
    return nx.community.modularity(G, [set(c) for c in communities])


def community_connectivity(G, communities) -> dict:
    """Do these communities actually hold together?

    Three failures, counted separately, in increasing order of how ordinary
    they are.

    ``disconnected``
        The community's own subgraph falls into more than one piece. Members
        reported as belonging together with no path between them *inside* the
        community. This is the failure the Leiden algorithm exists to prevent,
        and it is the serious one.

    ``fragile``
        Connected, but there is a single edge whose removal would split it into
        two parts of **at least two nodes each**. The community is genuinely
        two clumps joined by a thread.

    ``pendant``
        Connected, but some member is attached to its own community by exactly
        one edge - a leaf hanging off the side.

    Why three, and why ``pendant`` is reported separately
    -----------------------------------------------------
    An earlier version of this function counted any community with a leaf as
    "badly connected". That produced rates of 84% to 100% across every graph
    and every algorithm - which is not a finding, it is a definition that
    cannot discriminate. Almost every community in a sparse graph has a leaf
    somewhere.

    So ``pendant`` is still reported, because it is true and mildly
    interesting, but it is not the headline. ``fragile`` is the number that
    distinguishes one grouping from another, because it requires *both* sides
    of the cut to be substantial.

    A community is counted in at most one category, most-serious first.

    The denominator
    ---------------
    Communities of one or two nodes cannot be disconnected, fragile or pendant -
    there is nothing to say about them. They are excluded from the denominator
    and reported separately as ``n_communities`` vs ``n_assessed``.

    This matters: some graphs here produce hundreds of tiny communities, and
    dividing by all of them would report a reassuringly small rate that mostly
    measures how many communities were too small to be judged. **Every fraction
    below is over** ``n_assessed``.
    """
    communities = [set(c) for c in communities]
    n_disconnected = n_fragile = n_pendant = 0
    n_assessed = 0

    for community in communities:
        if len(community) <= 2:
            continue
        n_assessed += 1
        sub = G.subgraph(community)
        if sub.is_directed():
            sub = sub.to_undirected()

        if nx.number_connected_components(sub) > 1:
            n_disconnected += 1
            continue

        # A bridge that leaves two substantial pieces behind.
        #
        # Removing bridge (a, b) from a connected subgraph splits it in exactly
        # two: a's side and b's side. a's side has 2+ nodes precisely when a has
        # another neighbour inside the community - so an internal degree of 2 or
        # more on BOTH endpoints is equivalent to "both pieces are substantial",
        # and needs no subgraph copying to decide.
        degree = dict(sub.degree())
        fragile = any(degree[a] >= 2 and degree[b] >= 2
                      for a, b in nx.bridges(sub))
        if fragile:
            n_fragile += 1
            continue

        if any(d <= 1 for _, d in sub.degree()):
            n_pendant += 1

    scale = n_assessed if n_assessed else 1
    return {
        "n_communities": len(communities),
        "n_assessed": n_assessed,
        "n_disconnected": n_disconnected,
        "frac_disconnected": n_disconnected / scale,
        "n_fragile": n_fragile,
        "frac_fragile": n_fragile / scale,
        "n_pendant": n_pendant,
        "frac_pendant": n_pendant / scale,
    }
