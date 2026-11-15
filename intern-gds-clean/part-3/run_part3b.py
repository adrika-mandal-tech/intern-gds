"""Part 3B - do the communities actually hold together? And does similarity
find the edges that matter?

    python part-3/run_part3b.py --who <your-name>

Runs Louvain and Leiden 50 times each on five graphs, and for EVERY community
either produces, checks whether that community is actually connected inside
itself. A community whose members cannot reach each other without leaving the
community is a group that does not exist.

Then, separately: computes edge betweenness and neighbour-overlap similarity for
every edge, and asks what similarity says about the edges that carry the most
traffic.

Writes into your-work/<your-name>/part3/:

    community_quality.csv        one row per run - Louvain and Leiden
    ground_truth_scores.csv      how each run compares to the real departments
    similarity_vs_bridges.csv    every edge: betweenness rank and similarity
    charts/*.png

About 5 minutes.
"""

from __future__ import annotations

import argparse
import os
import sys
import time

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

import igraph as ig  # noqa: E402
import leidenalg  # noqa: E402
import networkx as nx  # noqa: E402

from gdslab import loaders, plots, runs, stats  # noqa: E402

GRAPHS = ["unicodelang", "crime", "email-Eu-core", "openflights", "ca-GrQc"]
SIM_GRAPHS = ["crime", "email-Eu-core"]
SEEDS = 50

QUALITY_FIELDS = ["graph", "algorithm", "seed", "n_nodes", "n_edges", "elapsed_s",
                  "n_communities", "n_assessed", "modularity", "n_disconnected",
                  "frac_disconnected", "n_fragile", "frac_fragile",
                  "n_pendant", "frac_pendant", "largest_community"]
TRUTH_FIELDS = ["graph", "algorithm", "seed", "n_communities", "modularity",
                "nmi_vs_truth", "ari_vs_truth"]
SIM_FIELDS = ["graph", "source", "target", "edge_betweenness", "betweenness_rank",
              "betweenness_pct", "jaccard_similarity", "shared_neighbours",
              "is_top_1pct"]


def to_igraph(G):
    names = sorted(G.nodes())
    index = {n: i for i, n in enumerate(names)}
    g = ig.Graph(n=len(names), edges=[(index[a], index[b]) for a, b in G.edges()],
                 directed=False)
    g.vs["name"] = names
    return g


def leiden_communities(g, seed):
    part = leidenalg.find_partition(g, leidenalg.ModularityVertexPartition,
                                    seed=seed)
    return [{g.vs[i]["name"] for i in cluster} for cluster in part]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    ap.add_argument("--seeds", type=int, default=SEEDS)
    args = ap.parse_args()

    outdir = os.path.join(BASE, "your-work", args.who, "part3")
    charts = os.path.join(outdir, "charts")
    os.makedirs(charts, exist_ok=True)

    info = runs.provenance()
    print("=" * 74)
    print("  Part 3B - do the communities hold together?")
    print("=" * 74)
    print("  machine : %s | %s cores" % (info["platform"], info["cpu_count"]))
    print("  %d seeds per algorithm per graph\n" % args.seeds)
    started = time.time()

    truth = loaders.ground_truth("email-Eu-core")
    disc_by_algo = {"louvain": [], "leiden": []}

    quality = runs.Recorder(os.path.join(outdir, "community_quality.csv"),
                            QUALITY_FIELDS)
    truth_rec = runs.Recorder(os.path.join(outdir, "ground_truth_scores.csv"),
                              TRUTH_FIELDS)

    for name in GRAPHS:
        G = loaders.load(name, weighted=False)
        if G.is_directed():
            G = G.to_undirected()
        n, m = G.number_of_nodes(), G.number_of_edges()
        g = to_igraph(G)
        print("  %-18s N=%-6d E=%-6d" % (name, n, m))

        for algorithm in ("louvain", "leiden"):
            disconnected_total = assessed_total = fragile_total = pendant_total = 0
            mods = []
            for seed in range(args.seeds):
                t0 = time.perf_counter()
                if algorithm == "louvain":
                    communities = nx.community.louvain_communities(G, seed=seed)
                else:
                    communities = leiden_communities(g, seed)
                elapsed = time.perf_counter() - t0

                conn = stats.community_connectivity(G, communities)
                q = stats.modularity(G, communities)
                mods.append(q)

                quality.row(
                    graph=name, algorithm=algorithm, seed=seed, n_nodes=n,
                    n_edges=m, elapsed_s=round(elapsed, 6),
                    n_communities=conn["n_communities"],
                    n_assessed=conn["n_assessed"], modularity=round(q, 6),
                    n_disconnected=conn["n_disconnected"],
                    frac_disconnected=round(conn["frac_disconnected"], 6),
                    n_fragile=conn["n_fragile"],
                    frac_fragile=round(conn["frac_fragile"], 6),
                    n_pendant=conn["n_pendant"],
                    frac_pendant=round(conn["frac_pendant"], 6),
                    largest_community=max(len(c) for c in communities))

                disconnected_total += conn["n_disconnected"]
                fragile_total += conn["n_fragile"]
                pendant_total += conn["n_pendant"]
                assessed_total += conn["n_assessed"]

                if name == "email-Eu-core":
                    labels = {node: i for i, c in enumerate(communities)
                              for node in c}
                    shared = {k: labels[k] for k in truth if k in labels}
                    truth_rec.row(
                        graph=name, algorithm=algorithm, seed=seed,
                        n_communities=len(communities), modularity=round(q, 6),
                        nmi_vs_truth=round(stats.nmi(truth, shared), 6),
                        ari_vs_truth=round(stats.adjusted_rand(truth, shared), 6))

            scale = assessed_total or 1
            rate = 100 * disconnected_total / scale
            frate = 100 * fragile_total / scale
            prate = 100 * pendant_total / scale
            disc_by_algo[algorithm].append(rate)
            print("     %-8s %6d assessable communities over %d runs"
                  % (algorithm, assessed_total, args.seeds))
            print("              disconnected %4d (%.2f%%) | fragile %5d (%.2f%%)"
                  " | pendant %5d (%.2f%%)"
                  % (disconnected_total, rate, fragile_total, frate,
                     pendant_total, prate))
        print()

    quality.close()
    truth_rec.close()

    # ---- similarity vs the edges that matter ---------------------------
    print("  Similarity on the edges that carry the most traffic")
    zero_sim_top = {}
    with runs.Recorder(os.path.join(outdir, "similarity_vs_bridges.csv"),
                       SIM_FIELDS) as rec:
        for name in SIM_GRAPHS:
            G = loaders.load(name, weighted=False)
            if G.is_directed():
                G = G.to_undirected()
            eb = nx.edge_betweenness_centrality(G)
            ranked = sorted(eb, key=lambda e: -eb[e])
            total = len(ranked)
            cutoff = max(1, int(total * 0.01))

            zeros = 0
            for rank, (a, b) in enumerate(ranked, start=1):
                na, nb = set(G[a]), set(G[b])
                shared = na & nb
                union = (na | nb) - {a, b}
                jac = len(shared) / len(union) if union else 0.0
                is_top = rank <= cutoff
                if is_top and jac == 0.0:
                    zeros += 1
                rec.row(graph=name, source=a, target=b,
                        edge_betweenness=round(eb[(a, b)], 10),
                        betweenness_rank=rank,
                        betweenness_pct=round(100 * rank / total, 4),
                        jaccard_similarity=round(jac, 6),
                        shared_neighbours=len(shared), is_top_1pct=is_top)
            zero_sim_top[name] = (zeros, cutoff)
            print("     %-18s top 1%% of edges = %d edges | "
                  "%d of them score similarity EXACTLY zero (%.1f%%)"
                  % (name, cutoff, zeros, 100 * zeros / cutoff))

    plots.bar(GRAPHS + GRAPHS,
              disc_by_algo["louvain"] + disc_by_algo["leiden"],
              "% of communities internally disconnected",
              "Louvain (left 5) vs Leiden (right 5), %d runs each" % args.seeds,
              os.path.join(charts, "disconnected_rate.png"))

    print("\n" + "=" * 74)
    print("  Done in %.0f s. Files in %s" % (time.time() - started, outdir))
    print("=" * 74)


if __name__ == "__main__":
    main()
