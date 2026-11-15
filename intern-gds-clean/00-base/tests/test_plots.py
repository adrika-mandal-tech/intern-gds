import networkx as nx

from gdslab import plots


def _made(path):
    return path.exists() and path.stat().st_size > 1000


def test_degree_distribution_writes_a_png(tmp_path):
    p = tmp_path / "deg.png"
    plots.degree_distribution(nx.barabasi_albert_graph(200, 3, seed=1), "ba", str(p))
    assert _made(p)


def test_scatter_writes_a_png(tmp_path):
    p = tmp_path / "sc.png"
    plots.scatter([1, 2, 3], [4, 5, 6], ["a", "b", "c"], "x", "y", "t", str(p))
    assert _made(p)


def test_box_writes_a_png(tmp_path):
    p = tmp_path / "box.png"
    plots.box({"a": [1, 2, 3, 4], "b": [2, 3, 4, 5]}, "y", "t", str(p))
    assert _made(p)


def test_bar_writes_a_png(tmp_path):
    p = tmp_path / "bar.png"
    plots.bar(["a", "b"], [1, 2], "y", "t", str(p))
    assert _made(p)


def test_line_writes_a_png(tmp_path):
    p = tmp_path / "line.png"
    plots.line([1, 2, 3], {"s1": [1, 2, 3], "s2": [3, 2, 1]}, "x", "y", "t", str(p))
    assert _made(p)


def test_creates_missing_parent_directory(tmp_path):
    p = tmp_path / "nested" / "deeper" / "b.png"
    plots.bar(["a"], [1], "y", "t", str(p))
    assert _made(p)
