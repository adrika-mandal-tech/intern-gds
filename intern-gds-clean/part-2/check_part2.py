"""Check your Part 2 deliverables.

    python part-2/check_part2.py --who <your-name> --track A
    python part-2/check_part2.py --who <your-name> --track B

Checks that your evidence is present and well-formed. It cannot check whether
your findings are true - see what it prints when it passes.
"""

from __future__ import annotations

import argparse
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

from gdslab import check  # noqa: E402

A_GRAPHS, B_GRAPHS = 5, 5
B_RUNS = 200

MEMO_SECTIONS = ["What I did", "What I found", "What surprised me",
                 "What I could not determine", "Judgement calls",
                 "Sample sizes", "Collaboration record"]


def track_a(d):
    scores = os.path.join(d, "centrality_scores.csv")
    agree = os.path.join(d, "centrality_agreement.csv")
    cost = os.path.join(d, "centrality_cost.csv")
    dis = os.path.join(d, "disagreements.csv")

    problems = []
    problems += check.require_columns(scores, [
        "graph", "node", "degree", "pagerank", "closeness", "betweenness"])
    problems += check.require_no_nulls(scores, ["graph", "node", "degree",
                                                "betweenness"])
    problems += check.require_provenance(scores)

    problems += check.require_columns(agree, [
        "graph", "measure_a", "measure_b", "spearman", "top10_overlap"])
    # 4 measures -> 6 unordered pairs per graph
    problems += check.require_min_rows(agree, A_GRAPHS * 6)
    problems += check.require_no_nulls(agree, ["spearman", "top10_overlap"])

    problems += check.require_columns(cost, ["graph", "measure", "elapsed_s"])
    problems += check.require_min_rows(cost, A_GRAPHS * 4)

    problems += check.require_columns(dis, [
        "graph", "node", "degree_rank", "betweenness_rank", "rank_gap"])
    problems += check.require_min_rows(dis, A_GRAPHS)
    return problems


def track_b(d):
    louvain = os.path.join(d, "louvain_runs.csv")
    problems = []
    problems += check.require_columns(louvain, [
        "graph", "seed", "elapsed_s", "n_communities", "modularity",
        "partition_hash", "ari_vs_run1"])
    problems += check.require_min_rows(louvain, B_GRAPHS * B_RUNS)
    problems += check.require_no_nulls(louvain, [
        "graph", "seed", "n_communities", "modularity", "partition_hash"])
    problems += check.require_distinct(louvain, "seed", B_RUNS, group_by="graph")
    problems += check.require_provenance(louvain)
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    ap.add_argument("--track", required=True, choices=["A", "B"])
    args = ap.parse_args()

    d = os.path.join(BASE, "your-work", args.who, "part2")
    problems = track_a(d) if args.track == "A" else track_b(d)

    memo = os.path.join(d, "part2-memo.md")
    problems += check.require_sections(memo, MEMO_SECTIONS)
    problems += check.require_no_placeholders(memo)
    problems += check.require_a_sample_size(memo)

    log = os.path.join(BASE, "your-work", args.who, "research-log.md")
    problems += check.file_exists(log, "research log")

    sys.exit(check.report("Part 2%s - %s" % (args.track, args.who), problems))


if __name__ == "__main__":
    main()
