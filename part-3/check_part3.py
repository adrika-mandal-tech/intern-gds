"""Check your Part 3 deliverables.

    python part-3/check_part3.py --who <your-name> --track A
    python part-3/check_part3.py --who <your-name> --track B
"""

from __future__ import annotations

import argparse
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

from gdslab import check  # noqa: E402

A_GRAPHS, FRACTIONS, A_SEEDS, N_PAIRS = 3, 5, 10, 500
B_GRAPHS, B_SEEDS, SIM_GRAPHS = 5, 50, 2

MEMO_SECTIONS = ["What I did", "What I found", "What surprised me",
                 "What I could not determine", "Judgement calls",
                 "Sample sizes", "Collaboration record"]


def track_a(d):
    exact = os.path.join(d, "betweenness_exact.csv")
    approx = os.path.join(d, "betweenness_approx.csv")
    weights = os.path.join(d, "weights_effect.csv")

    problems = []
    problems += check.require_columns(exact, ["graph", "n_nodes", "elapsed_s",
                                              "per_pivot_ms"])
    problems += check.require_min_rows(exact, A_GRAPHS)
    problems += check.require_provenance(exact)

    problems += check.require_columns(approx, [
        "graph", "fraction", "k_pivots", "seed", "elapsed_s",
        "top10_overlap", "top50_overlap", "spearman"])
    problems += check.require_min_rows(approx, A_GRAPHS * FRACTIONS * A_SEEDS)
    problems += check.require_no_nulls(approx, ["top10_overlap", "spearman"])
    problems += check.require_distinct(approx, "seed", A_SEEDS, group_by="graph")

    problems += check.require_columns(weights, [
        "pair", "source", "target", "hops_path_cost_km", "cheap_path_cost_km",
        "paths_differ", "cost_ratio"])
    problems += check.require_min_rows(weights, N_PAIRS)
    problems += check.require_no_nulls(weights, ["cost_ratio", "paths_differ"])
    return problems


def track_b(d):
    quality = os.path.join(d, "community_quality.csv")
    truth = os.path.join(d, "ground_truth_scores.csv")
    sim = os.path.join(d, "similarity_vs_bridges.csv")

    problems = []
    problems += check.require_columns(quality, [
        "graph", "algorithm", "seed", "n_communities", "n_assessed",
        "modularity", "n_disconnected", "frac_disconnected", "n_fragile",
        "frac_fragile", "n_pendant"])
    # 5 graphs x 2 algorithms x 50 seeds
    problems += check.require_min_rows(quality, B_GRAPHS * 2 * B_SEEDS)
    problems += check.require_no_nulls(quality, ["graph", "algorithm",
                                                 "n_disconnected", "n_fragile"])
    problems += check.require_provenance(quality)

    problems += check.require_columns(truth, [
        "graph", "algorithm", "seed", "nmi_vs_truth", "ari_vs_truth"])
    problems += check.require_min_rows(truth, 2 * B_SEEDS)

    problems += check.require_columns(sim, [
        "graph", "source", "target", "edge_betweenness", "betweenness_rank",
        "jaccard_similarity", "is_top_1pct"])
    problems += check.require_min_rows(sim, 1000)
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    ap.add_argument("--track", required=True, choices=["A", "B"])
    args = ap.parse_args()

    d = os.path.join(BASE, "your-work", args.who, "part3")
    problems = track_a(d) if args.track == "A" else track_b(d)

    memo = os.path.join(d, "part3-memo.md")
    problems += check.require_sections(memo, MEMO_SECTIONS)
    problems += check.require_no_placeholders(memo)
    problems += check.require_a_sample_size(memo)

    log = os.path.join(BASE, "your-work", args.who, "research-log.md")
    problems += check.file_exists(log, "research log")

    sys.exit(check.report("Part 3%s - %s" % (args.track, args.who), problems))


if __name__ == "__main__":
    main()
