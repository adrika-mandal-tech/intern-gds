"""Part 2B - is community detection repeatable?

    python part-2/run_part2b.py --who <your-name>

Runs Louvain 200 times per graph, with a different seed each time, and records
what came out. Nothing is compared to anything else here: the only question is
how much one algorithm varies with ITSELF on identical input.

Writes into your-work/<your-name>/part2/:

    louvain_runs.csv      200 rows per graph - one per run, never a summary
    charts/*.png

About three minutes.
"""

from __future__ import annotations

import argparse
import os
import statistics
import sys
import time

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

import networkx as nx  # noqa: E402

from gdslab import loaders, plots, runs, stats  # noqa: E402

GRAPHS = ["unicodelang", "crime", "email-Eu-core", "openflights", "ca-GrQc"]
N_RUNS = 200

FIELDS = ["graph", "seed", "n_nodes", "n_edges", "elapsed_s", "n_communities",
          "modularity", "partition_hash", "ari_vs_run1", "largest_community"]


def as_labels(communities):
    return {node: i for i, community in enumerate(communities) for node in community}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    ap.add_argument("--runs", type=int, default=N_RUNS)
    args = ap.parse_args()

    outdir = os.path.join(BASE, "your-work", args.who, "part2")
    charts = os.path.join(outdir, "charts")
    os.makedirs(charts, exist_ok=True)

    info = runs.provenance()
    print("=" * 74)
    print("  Part 2B - is community detection repeatable?")
    print("=" * 74)
    print("  machine : %s | %s cores" % (info["platform"], info["cpu_count"]))
    print("  %d runs per graph, %d graphs\n" % (args.runs, len(GRAPHS)))

    modularity_spread = {}
    started = time.time()

    with runs.Recorder(os.path.join(outdir, "louvain_runs.csv"), FIELDS) as rec:
        for name in GRAPHS:
            G = loaders.load(name, weighted=False)
            if G.is_directed():
                G = G.to_undirected()
            n, m = G.number_of_nodes(), G.number_of_edges()

            first_labels = None
            counts, mods, hashes, aris = [], [], set(), []

            nx.community.louvain_communities(G, seed=999)  # warm up

            for seed in range(args.runs):
                t0 = time.perf_counter()
                communities = nx.community.louvain_communities(G, seed=seed)
                elapsed = time.perf_counter() - t0

                labels = as_labels(communities)
                if first_labels is None:
                    first_labels = labels
                    ari = 1.0
                else:
                    ari = stats.adjusted_rand(first_labels, labels)

                q = stats.modularity(G, communities)
                digest = stats.partition_hash(communities)
                largest = max(len(c) for c in communities)

                rec.row(graph=name, seed=seed, n_nodes=n, n_edges=m,
                        elapsed_s=round(elapsed, 6),
                        n_communities=len(communities),
                        modularity=round(q, 6), partition_hash=digest,
                        ari_vs_run1=round(ari, 6), largest_community=largest)

                counts.append(len(communities))
                mods.append(q)
                hashes.add(digest)
                aris.append(ari)

            modularity_spread[name] = mods
            distinct = len(hashes)
            print("  %-18s N=%-6d E=%-6d" % (name, n, m))
            print("     communities   min=%-4d max=%-4d  (%d distinct counts)"
                  % (min(counts), max(counts), len(set(counts))))
            print("     modularity    min=%.4f max=%.4f  spread=%.4f  sd=%.5f"
                  % (min(mods), max(mods), max(mods) - min(mods),
                     statistics.pstdev(mods)))
            print("     distinct partitions: %d of %d runs" % (distinct, args.runs))
            print("     mean ARI vs run 1  : %.4f    identical to run 1: %d/%d"
                  % (sum(aris) / len(aris),
                     sum(1 for a in aris if a == 1.0), args.runs))
            print()

    plots.box(modularity_spread, "modularity",
              "Modularity across %d runs on identical input" % args.runs,
              os.path.join(charts, "modularity_spread.png"))

    print("=" * 74)
    print("  Done in %.0f s. Files in %s" % (time.time() - started, outdir))
    print("=" * 74)
    print("\n  Read those 'distinct partitions' lines again.")
    print("  Same graph, same algorithm, same input - one number changed.")
    print("\n  Now: is a different partition a WORSE partition? The modularity")
    print("  spread is how you answer that, and it is not the same question.")


if __name__ == "__main__":
    main()
