"""Part 1 — profile the zoo, then find out what actually predicts cost.

    python part-1/run_part1.py --who <your-name>

Writes into your-work/<your-name>/part1/:

    profiles.csv          the shape of all seven graphs
    pagerank_runs.csv     10 timed runs of PageRank per graph
    charts/*.png

Takes about a minute. Nothing here is expensive; Part 1 is about learning to
measure, not about waiting.
"""

from __future__ import annotations

import argparse
import os
import statistics
import sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

from gdslab import algos, loaders, plots, profile, runs  # noqa: E402

RUNS_PER_GRAPH = 10

PROFILE_FIELDS = profile.FIELDS
PAGERANK_FIELDS = ["graph", "run", "n_nodes", "n_edges", "degree_skew",
                   "load_s", "compute_s", "iterations", "top_node",
                   "top_score", "scores_hash"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True,
                    help="your name - results go to your-work/<who>/part1/")
    args = ap.parse_args()

    outdir = os.path.join(BASE, "your-work", args.who, "part1")
    charts = os.path.join(outdir, "charts")
    os.makedirs(charts, exist_ok=True)

    info = runs.provenance()
    print("=" * 74)
    print("  Part 1 - measuring the graphs before measuring the algorithms")
    print("=" * 74)
    print("  machine : %s | %s cores | %s GB RAM"
          % (info["platform"], info["cpu_count"], info["ram_gb"]))
    print("  writing : %s" % outdir)

    bad = loaders.verify_checksums()
    if bad:
        sys.exit("data files do not match their checksums: %s" % bad)

    graph_names = sorted(loaders.list_graphs(),
                         key=lambda n: loaders.describe(n)["nodes"])

    # ---- experiment 1.1 : profile every graph ---------------------------
    print("\n1.1  Profiling every graph")
    print("     %-20s %7s %8s %7s %7s %7s"
          % ("graph", "nodes", "edges", "skew", "comps", "clust"))

    graphs = {}
    with runs.Recorder(os.path.join(outdir, "profiles.csv"), PROFILE_FIELDS) as rec:
        for name in graph_names:
            G = loaders.load(name)
            graphs[name] = G
            p = profile.profile_graph(G, name)
            rec.row(**p)
            print("     %-20s %7d %8d %7.1f %7d %7.3f"
                  % (name, p["nodes"], p["edges"], p["degree_skew"],
                     p["components"], p["clustering"]))
            plots.degree_distribution(
                G, name, os.path.join(charts, "degree_%s.png" % name))

    # ---- experiment 1.2 : what predicts cost? ---------------------------
    print("\n1.2  PageRank on each graph, %d runs each" % RUNS_PER_GRAPH)
    print("     %-20s %9s %9s %7s %9s"
          % ("graph", "load_s", "compute_s", "rounds", "identical?"))

    summary = {}
    with runs.Recorder(os.path.join(outdir, "pagerank_runs.csv"),
                       PAGERANK_FIELDS) as rec:
        for name in graph_names:
            p = profile.profile_graph(graphs[name], name)
            computes, iterations, hashes = [], [], set()

            for run_index in range(RUNS_PER_GRAPH):
                load_s, G = runs.timed(loaders.load, name, warmup=0 if run_index else 1)
                compute_s, (scores, iters) = runs.timed(
                    algos.pagerank_iters, G, warmup=1 if run_index == 0 else 0)

                top_node = max(scores, key=lambda k: (scores[k], str(k)))
                digest = hash(tuple(round(scores[k], 12) for k in sorted(scores)))
                hashes.add(digest)
                computes.append(compute_s)
                iterations.append(iters)

                rec.row(graph=name, run=run_index, n_nodes=p["nodes"],
                        n_edges=p["edges"], degree_skew=round(p["degree_skew"], 3),
                        load_s=round(load_s, 6), compute_s=round(compute_s, 6),
                        iterations=iters, top_node=top_node,
                        top_score=round(scores[top_node], 8),
                        scores_hash=digest)

            summary[name] = dict(
                nodes=p["nodes"], edges=p["edges"], skew=p["degree_skew"],
                compute=statistics.median(computes), iters=iterations[0],
                stable=len(hashes) == 1)
            print("     %-20s %9.4f %9.4f %7d %9s"
                  % (name, load_s, statistics.median(computes), iterations[0],
                     "yes" if len(hashes) == 1 else "NO"))

    # ---- charts ----------------------------------------------------------
    names = list(summary)
    plots.scatter([summary[n]["nodes"] for n in names],
                  [summary[n]["compute"] for n in names], names,
                  "nodes", "PageRank compute time (s, median of %d)" % RUNS_PER_GRAPH,
                  "Does node count predict cost?",
                  os.path.join(charts, "cost_vs_nodes.png"), logx=True, logy=True)
    plots.scatter([summary[n]["edges"] for n in names],
                  [summary[n]["compute"] for n in names], names,
                  "edges", "PageRank compute time (s, median of %d)" % RUNS_PER_GRAPH,
                  "Does edge count predict cost?",
                  os.path.join(charts, "cost_vs_edges.png"), logx=True, logy=True)
    plots.scatter([summary[n]["skew"] for n in names],
                  [summary[n]["iters"] for n in names], names,
                  "degree skew (max / median)", "rounds to converge",
                  "Does lopsidedness predict the number of rounds?",
                  os.path.join(charts, "rounds_vs_skew.png"), logx=True)
    plots.scatter([summary[n]["nodes"] for n in names],
                  [summary[n]["iters"] for n in names], names,
                  "nodes", "rounds to converge",
                  "Does node count predict the number of rounds?",
                  os.path.join(charts, "rounds_vs_nodes.png"), logx=True)

    # ---- what the numbers say -------------------------------------------
    print("\n" + "=" * 74)
    print("  Done. Now go and interpret it - that part is yours.")
    print("=" * 74)

    biggest = max(names, key=lambda n: summary[n]["nodes"])
    slowest = max(names, key=lambda n: summary[n]["compute"])
    print("\n  Most nodes  : %-20s (%d nodes)" % (biggest, summary[biggest]["nodes"]))
    print("  Slowest     : %-20s (%d nodes)" % (slowest, summary[slowest]["nodes"]))
    if biggest != slowest:
        print("\n  Those are not the same graph. Section 2 of your memo should")
        print("  explain why, and say what DOES predict the cost.")

    unstable = [n for n in names if not summary[n]["stable"]]
    print("\n  PageRank gave identical scores across all %d runs on %d of %d graphs."
          % (RUNS_PER_GRAPH, len(names) - len(unstable), len(names)))
    if unstable:
        print("  NOT identical on: %s  <- that is a finding, write it up" % unstable)
    else:
        print("  Worth remembering when you meet an algorithm that does not.")

    print("\n  Files written to %s" % outdir)
    print("  Next: compare your numbers with your colleague's. See the brief.")


if __name__ == "__main__":
    main()
