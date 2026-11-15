"""Charts.

Deliberately plain. A chart in a memo is there to make a number easier to
believe, not to look impressive - so every one of these labels its axes, states
its sample size where it has one, and uses a log scale when the data spans
orders of magnitude (which graph data usually does).

All functions write a PNG and return its path.
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")  # no display needed; must be set before pyplot is imported
import matplotlib.pyplot as plt  # noqa: E402

_FIGSIZE = (7.0, 4.5)
_DPI = 130


def _finish(fig, ax, title, xlabel, ylabel, path):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.25, linewidth=0.6)
    fig.tight_layout()
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    fig.savefig(path, dpi=_DPI)
    plt.close(fig)
    return path


def degree_distribution(G, name: str, path: str) -> str:
    """How lopsided is this graph? Log-log, because the tail is the point."""
    degrees = sorted((d for _, d in G.degree()), reverse=True)
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.plot(range(1, len(degrees) + 1), degrees, marker=".", linestyle="none",
            markersize=3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    return _finish(fig, ax,
                   "%s - degree distribution (n=%d)" % (name, len(degrees)),
                   "node, ranked by degree", "degree", path)


def scatter(xs, ys, labels, xlabel: str, ylabel: str, title: str, path: str,
            logx: bool = False, logy: bool = False) -> str:
    """Scatter with a text label on every point - you want to see which is which."""
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.plot(xs, ys, marker="o", linestyle="none", markersize=6)
    for x, y, label in zip(xs, ys, labels):
        ax.annotate(str(label), (x, y), textcoords="offset points",
                    xytext=(5, 4), fontsize=7)
    if logx:
        ax.set_xscale("log")
    if logy:
        ax.set_yscale("log")
    return _finish(fig, ax, title, xlabel, ylabel, path)


def box(groups: dict, ylabel: str, title: str, path: str) -> str:
    """One box per group. Use this whenever you have many runs of the same thing."""
    labels = list(groups)
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.boxplot([groups[k] for k in labels], tick_labels=labels)
    ax.tick_params(axis="x", labelrotation=20, labelsize=8)
    return _finish(fig, ax, title, "", ylabel, path)


def bar(labels, values, ylabel: str, title: str, path: str) -> str:
    """Plain bar chart."""
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    ax.bar([str(x) for x in labels], values)
    ax.tick_params(axis="x", labelrotation=20, labelsize=8)
    return _finish(fig, ax, title, "", ylabel, path)


def line(xs, series: dict, xlabel: str, ylabel: str, title: str, path: str,
         logx: bool = False) -> str:
    """One line per named series, sharing an x axis."""
    fig, ax = plt.subplots(figsize=_FIGSIZE)
    for label, ys in series.items():
        ax.plot(xs, ys, marker="o", markersize=4, label=str(label))
    if logx:
        ax.set_xscale("log")
    ax.legend(fontsize=8)
    return _finish(fig, ax, title, xlabel, ylabel, path)
