"""Part 3A - what does betweenness cost, and can you get away with sampling it?
Plus: how wrong are you if you ignore edge weights?

    python part-3/run_part3a.py --who <your-name>
    python part-3/run_part3a.py --who <your-name> --full   # adds facebook_combined

Writes into your-work/<your-name>/part3/:

    betweenness_exact.csv     the ground truth, and what it cost
    betweenness_approx.csv    sampled at 5 fractions x 10 seeds
    weights_effect.csv        500 routes, computed with and without weights
    charts/*.png

About 8 minutes (--full is about 25). Start it, then read the brief while it runs.
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

import networkx as nx  # noqa: E402

from gdslab import loaders, plots, runs, stats  # noqa: E402

GRAPHS = ["email-Eu-core", "openflights", "ca-GrQc"]
FRACTIONS = [0.01, 0.02, 0.05, 0.10, 0.25]
SEEDS = 10
N_PAIRS = 500

EXACT_FIELDS = ["graph", "n_nodes", "n_edges", "elapsed_s", "per_pivot_ms"]
APPROX_FIELDS = ["graph", "fraction", "k_pivots", "seed", "elapsed_s",
                 "speedup_vs_exact", "top10_overlap", "top50_overlap", "spearman"]
WEIGHT_FIELDS = ["pair", "source", "target", "hops_path_len", "hops_path_cost_km",
                 "cheap_path_len", "cheap_path_cost_km", "paths_differ",
                 "cost_ratio", "extra_km"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    ap.add_argument("--full", action="store_true",
                    help="also run facebook_combined (much slower)")
    args = ap.parse_args()

    graphs = GRAPHS + (["facebook_combined"] if args.full else [])
    outdir = os.path.join(BASE, "your-work", args.who, "part3")
    charts = os.path.join(outdir, "charts")
    os.makedirs(charts, exist_ok=True)

    info = runs.provenance()
    print("=" * 74)
    print("  Part 3A - betweenness cost, approximation, and weights")
    print("=" * 74)
    print("  machine : %s | %s cores" % (info["platform"], info["cpu_count"]))
    started = time.time()

    # ---- 1. exact betweenness ------------------------------------------
    print("\n1. Exact betweenness (the ground truth to compare against)")
    exact_scores, exact_time = {}, {}
    with runs.Recorder(os.path.join(outdir, "betweenness_exact.csv"),
                       EXACT_FIELDS) as rec:
        for name in graphs:
            G = loaders.load(name, weighted=False)
            if G.is_directed():
                G = G.to_undirected()
            n = G.number_of_nodes()
            t0 = time.perf_counter()
            scores = nx.betweenness_centrality(G)
            elapsed = time.perf_counter() - t0
            exact_scores[name], exact_time[name] = scores, elapsed
            rec.row(graph=name, n_nodes=n, n_edges=G.number_of_edges(),
                    elapsed_s=round(elapsed, 4),
                    per_pivot_ms=round(elapsed / n * 1000, 5))
            print("   %-20s N=%-6d %8.1f s   (%.4f ms per node)"
                  % (name, n, elapsed, elapsed / n * 1000))

    # ---- 2. sampled betweenness ----------------------------------------
    print("\n2. Sampled betweenness - %d fractions x %d seeds"
          % (len(FRACTIONS), SEEDS))
    by_fraction = {f: [] for f in FRACTIONS}
    with runs.Recorder(os.path.join(outdir, "betweenness_approx.csv"),
                       APPROX_FIELDS) as rec:
        for name in graphs:
            G = loaders.load(name, weighted=False)
            if G.is_directed():
                G = G.to_undirected()
            n = G.number_of_nodes()
            print("   %s" % name)
            for fraction in FRACTIONS:
                k = max(2, int(round(fraction * n)))
                overlaps = []
                for seed in range(SEEDS):
                    t0 = time.perf_counter()
                    approx = nx.betweenness_centrality(G, k=k, seed=seed)
                    elapsed = time.perf_counter() - t0
                    ov10 = stats.top_k_overlap(exact_scores[name], approx, 10)
                    ov50 = stats.top_k_overlap(exact_scores[name], approx, 50)
                    rho = stats.spearman(exact_scores[name], approx)
                    rec.row(graph=name, fraction=fraction, k_pivots=k, seed=seed,
                            elapsed_s=round(elapsed, 4),
                            speedup_vs_exact=round(exact_time[name] / elapsed, 2),
                            top10_overlap=round(ov10, 4),
                            top50_overlap=round(ov50, 4), spearman=round(rho, 4))
                    overlaps.append(ov10)
                mean_ov = sum(overlaps) / len(overlaps)
                by_fraction[fraction].append(mean_ov)
                print("      %5.0f%%  k=%-5d  mean top-10 overlap %.2f  "
                      "(worst %.2f)" % (fraction * 100, k, mean_ov, min(overlaps)))

    plots.line([f * 100 for f in FRACTIONS],
               {"mean top-10 overlap": [sum(by_fraction[f]) / len(by_fraction[f])
                                        for f in FRACTIONS]},
               "sample size (% of nodes)", "overlap with exact top 10",
               "How much sampling is enough? (mean over %d graphs)" % len(graphs),
               os.path.join(charts, "approx_quality.png"))

    # ---- 3. do weights matter? -----------------------------------------
    print("\n3. Ignoring edge weights - %d random airport pairs" % N_PAIRS)
    F = loaders.load("openflights").to_undirected()

    def cost(path):
        return sum(F[path[i]][path[i + 1]]["weight"] for i in range(len(path) - 1))

    rng = random.Random(20260817)
    candidates = [n for n in F if F.degree(n) >= 1]
    differ = same_hops_worse = 0
    ratios = []

    with runs.Recorder(os.path.join(outdir, "weights_effect.csv"),
                       WEIGHT_FIELDS) as rec:
        pair_index = 0
        attempts = 0
        while pair_index < N_PAIRS and attempts < N_PAIRS * 40:
            attempts += 1
            a, b = rng.sample(candidates, 2)
            if not nx.has_path(F, a, b):
                continue
            hop_path = nx.shortest_path(F, a, b)
            cheap_path = nx.shortest_path(F, a, b, weight="weight")
            hop_cost, cheap_cost = cost(hop_path), cost(cheap_path)
            differs = hop_path != cheap_path
            ratio = hop_cost / cheap_cost if cheap_cost else 1.0
            rec.row(pair=pair_index, source=a, target=b,
                    hops_path_len=len(hop_path) - 1,
                    hops_path_cost_km=round(hop_cost, 1),
                    cheap_path_len=len(cheap_path) - 1,
                    cheap_path_cost_km=round(cheap_cost, 1),
                    paths_differ=differs, cost_ratio=round(ratio, 4),
                    extra_km=round(hop_cost - cheap_cost, 1))
            if differs:
                differ += 1
                ratios.append(ratio)
                if len(hop_path) == len(cheap_path):
                    same_hops_worse += 1
            pair_index += 1

    ratios.sort()
    print("   routes where the two answers differ : %d of %d (%.1f%%)"
          % (differ, N_PAIRS, 100 * differ / N_PAIRS))
    if ratios:
        print("   of those, cost ratio (hops answer / best answer):")
        print("      median %.2fx   90th pct %.2fx   worst %.2fx"
              % (ratios[len(ratios) // 2], ratios[int(len(ratios) * 0.9)],
                 ratios[-1]))
        print("   differed with NO saving in hops   : %d (%.1f%% of differing)"
              % (same_hops_worse, 100 * same_hops_worse / differ))

    plots.box({"cost ratio": ratios}, "hops-answer cost / best cost",
              "How much further do you fly by ignoring distance? (n=%d)" % len(ratios),
              os.path.join(charts, "weights_cost_ratio.png"))

    print("\n" + "=" * 74)
    print("  Done in %.0f s. Files in %s" % (time.time() - started, outdir))
    print("=" * 74)


if __name__ == "__main__":
    main()
