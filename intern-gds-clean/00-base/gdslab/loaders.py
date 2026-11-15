"""Load the graphs that ship with this pack.

Every graph lives in ``03-data/`` as a plain CSV edge list, and every file is
listed in ``03-data/MANIFEST.json`` together with where it came from, what
licence it carries, and its SHA-256.

Nothing here downloads anything. The pack works offline.

Why the checksums matter
------------------------
If you edit a data file by accident - open it in Excel, save it, and Excel
helpfully reformats a column - every number you measured afterwards is quietly
about a different graph. ``verify_checksums()`` catches that. ``check_setup.py``
runs it, and so should you if a result ever stops making sense.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os

import networkx as nx

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "03-data")
_MANIFEST_PATH = os.path.join(DATA_DIR, "MANIFEST.json")


def _manifest() -> dict:
    with open(_MANIFEST_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def _entries() -> dict:
    """Graph entries only, keyed by name (the label/side sidecars are excluded)."""
    return {e["name"]: e for e in _manifest()["entries"] if "edges" in e}


def _sidecars() -> dict:
    """Sidecar entries (ground-truth labels, bipartite sides), keyed by file name."""
    return {e["file"]: e for e in _manifest()["entries"] if "kind" in e}


def list_graphs() -> list:
    """Names of every graph that ships with the pack."""
    return sorted(_entries())


def describe(name: str) -> dict:
    """The manifest entry for one graph - source, licence, counts, checksum."""
    entries = _entries()
    if name not in entries:
        raise KeyError("no such graph %r; have %s" % (name, list_graphs()))
    return dict(entries[name])


def _path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_checksums() -> list:
    """Return the names of any files whose contents no longer match the manifest.

    An empty list means every shipped data file is byte-for-byte what it should be.
    """
    bad = []
    for entry in _manifest()["entries"]:
        path = _path(entry["file"])
        if not os.path.exists(path) or _sha256(path) != entry["sha256"]:
            bad.append(entry["name"])
    return bad


def load(name: str, *, directed: bool | None = None, weighted: bool = True):
    """Load a graph as a networkx graph.

    Parameters
    ----------
    name
        One of :func:`list_graphs`.
    directed
        By default the graph's own directedness is used (from the manifest).
        Pass ``False`` to collapse a directed graph to undirected - note that
        this merges reciprocal edges, so the edge count drops.
    weighted
        When the graph carries weights, attach them as the ``weight`` edge
        attribute. Pass ``False`` to deliberately throw the weights away, which
        is exactly the mistake one of the experiments asks you to measure.
    """
    entry = describe(name)
    if directed is None:
        directed = entry["directed"]

    G = nx.DiGraph() if directed else nx.Graph()
    use_weight = weighted and entry["weighted"]

    with open(_path(entry["file"]), encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        has_weight_col = "weight" in header
        for row in reader:
            if not row:
                continue
            if use_weight and has_weight_col:
                G.add_edge(row[0], row[1], weight=float(row[2]))
            else:
                G.add_edge(row[0], row[1])
    return G


def load_igraph(name: str):
    """Load a graph as an igraph graph - always undirected and unweighted.

    igraph is here because ``leidenalg`` needs it. Node names are preserved on
    the ``name`` vertex attribute so results can be mapped back.
    """
    import igraph as ig

    G = load(name, weighted=False)
    if G.is_directed():
        G = G.to_undirected()
    names = sorted(G.nodes())
    index = {n: i for i, n in enumerate(names)}
    g = ig.Graph(n=len(names), edges=[(index[a], index[b]) for a, b in G.edges()],
                 directed=False)
    g.vs["name"] = names
    return g


def sides(name: str) -> dict:
    """Bipartite side labels: ``{node: 0 or 1}``.

    Raises ``KeyError`` for a graph that is not bipartite.

    The sides were derived structurally, by two-colouring the graph, rather than
    read off a metadata column - because on both bipartite graphs in this pack
    the metadata column means something else entirely (in one it is gender, in
    the other a country code).
    """
    entry = describe(name)
    if not entry.get("bipartite"):
        raise KeyError("%r is not bipartite; bipartite graphs are %s"
                       % (name, [n for n, e in _entries().items() if e.get("bipartite")]))
    out = {}
    with open(_path(entry["side_file"]), encoding="utf-8") as fh:
        reader = csv.reader(fh)
        next(reader)
        for node, side in reader:
            out[node] = int(side)
    return out


def names(name: str) -> dict:
    """Human-readable node names: ``{node_id: name}``.

    Only some graphs have these, and they are **not** community labels - they
    are just what the thing is called. `lesmis` has them so that the smallest
    graph in the pack is one you can actually read: node 11 is Valjean, and if
    an algorithm tells you node 11 is the most important character you are in a
    position to agree or disagree with it.

    Raises ``KeyError`` for a graph that has none.
    """
    filename = "%s.names.csv" % name
    if filename not in _sidecars():
        have = [f[:-len(".names.csv")] for f in _sidecars() if f.endswith(".names.csv")]
        raise KeyError("%r has no node names; graphs that do: %s" % (name, have))
    out = {}
    with open(_path(filename), encoding="utf-8") as fh:
        reader = csv.reader(fh)
        next(reader)
        for node, label in reader:
            out[node] = label
    return out


def ground_truth(name: str) -> dict:
    """Known-correct community labels: ``{node: label}``.

    Raises ``KeyError`` for a graph that has none. Only one graph in this pack
    carries ground truth, and it is the only one on which you can score whether
    an algorithm is *right* rather than merely whether two algorithms *agree*.
    """
    filename = "%s.labels.csv" % name
    if filename not in _sidecars():
        have = [f[:-len(".labels.csv")] for f in _sidecars() if f.endswith(".labels.csv")]
        raise KeyError("%r has no ground truth; graphs that do: %s" % (name, have))
    out = {}
    with open(_path(filename), encoding="utf-8") as fh:
        reader = csv.reader(fh)
        next(reader)
        for node, label in reader:
            out[node] = label
    return out
