"""Part 2A - do the four centrality measures agree?

    python part-2/run_part2a.py --who <your-name>

Writes into your-work/<your-name>/part2/:

    centrality_scores.csv      every node's four scores, on every graph
    centrality_agreement.csv   pairwise Spearman and top-10 overlap
    centrality_cost.csv        what each measure cost to compute
    disagreements.csv          the nodes where cheap and expensive disagree most
    charts/*.png

About 90 seconds, nearly all of it exact betweenness on openflights.
"""

from __future__ import annotations

import argparse
import itertools
import os
import sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

import networkx as nx  # noqa: E402

from gdslab import loaders, plots, runs, stats  # noqa: E402

GRAPHS = ["lesmis", "unicodelang", "crime", "email-Eu-core", "openflights"]
MEASURES = ["degree", "pagerank", "closeness", "betweenness"]

SCORE_FIELDS = ["graph", "node", "degree", "pagerank", "closeness", "betweenness"]
AGREE_FIELDS = ["graph", "measure_a", "measure_b", "spearman", "top10_overlap"]
COST_FIELDS = ["graph", "n_nodes", "n_edges", "measure", "elapsed_s"]
DISAGREE_FIELDS = ["graph", "node", "degree", "degree_rank", "betweenness",
                   "betweenness_rank", "rank_gap", "direction"]


def compute(G):
    """The four measures, each timed. Returns (scores_by_measure, seconds)."""
    out, cost = {}, {}
    cost["degree"], out["degree"] = runs.timed(lambda: dict(G.degree()))
    cost["pagerank"], out["pagerank"] = runs.timed(nx.pagerank, G)
    cost["closeness"], out["closeness"] = runs.timed(nx.closeness_centrality, G)
    cost["betweenness"], out["betweenness"] = runs.timed(
        nx.betweenness_centrality, G)
    return out, cost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    args = ap.parse_args()

    outdir = os.path.join(BASE, "your-work", args.who, "part2")
    charts = os.path.join(outdir, "charts")
    os.makedirs(charts, exist_ok=True)

    info = runs.provenance()
    print("=" * 74)
    print("  Part 2A - do the four centrality measures agree?")
    print("=" * 74)
    print("  machine : %s | %s cores" % (info["platform"], info["cpu_count"]))

    scores_rec = runs.Recorder(os.path.join(outdir, "centrality_scores.csv"),
                               SCORE_FIELDS)
    agree_rec = runs.Recorder(os.path.join(outdir, "centrality_agreement.csv"),
                              AGREE_FIELDS)
    cost_rec = runs.Recorder(os.path.join(outdir, "centrality_cost.csv"),
                             COST_FIELDS)
    dis_rec = runs.Recorder(os.path.join(outdir, "disagreements.csv"),
                            DISAGREE_FIELDS)

    agreement_by_pair = {p: [] for p in itertools.combinations(MEASURES, 2)}

    for name in GRAPHS:
        G = loaders.load(name, weighted=False)
        if G.is_directed():
            G = G.to_undirected()
        n, m = G.number_of_nodes(), G.number_of_edges()
        print("\n  %s  (N=%d, E=%d)" % (name, n, m))

        scores, cost = compute(G)
        for measure in MEASURES:
            cost_rec.row(graph=name, n_nodes=n, n_edges=m, measure=measure,
                         elapsed_s=round(cost[measure], 6))
        print("     cost: " + "  ".join("%s %.3fs" % (k, cost[k])
                                        for k in MEASURES))

        for node in sorted(G):
            scores_rec.row(graph=name, node=node,
                           degree=scores["degree"][node],
                           pagerank=round(scores["pagerank"][node], 10),
                           closeness=round(scores["closeness"][node], 10),
                           betweenness=round(scores["betweenness"][node], 10))

        print("     agreement (Spearman / top-10 overlap):")
        for a, b in itertools.combinations(MEASURES, 2):
            rho = stats.spearman(scores[a], scores[b])
            ov = stats.top_k_overlap(scores[a], scores[b], 10)
            agree_rec.row(graph=name, measure_a=a, measure_b=b,
                          spearman=round(rho, 4), top10_overlap=round(ov, 4))
            agreement_by_pair[(a, b)].append(rho)
            print("       %-12s vs %-12s  rho=%+.3f  top10=%.2f" % (a, b, rho, ov))

        # where do the cheapest and the most expensive measure disagree most?
        def ranks(d):
            order = sorted(d, key=lambda k: (-d[k], str(k)))
            return {k: i + 1 for i, k in enumerate(order)}

        rd, rb = ranks(scores["degree"]), ranks(scores["betweenness"])
        gaps = sorted(G, key=lambda k: -abs(rd[k] - rb[k]))[:5]
        for node in gaps:
            dis_rec.row(graph=name, node=node,
                        degree=scores["degree"][node], degree_rank=rd[node],
                        betweenness=round(scores["betweenness"][node], 8),
                        betweenness_rank=rb[node],
                        rank_gap=abs(rd[node] - rb[node]),
                        direction=("betweenness ranks it higher"
                                   if rb[node] < rd[node]
                                   else "degree ranks it higher"))
        worst = gaps[0]
        print("     biggest degree-vs-betweenness disagreement: node %s "
              "(degree rank %d, betweenness rank %d)"
              % (worst, rd[worst], rb[worst]))

    for rec in (scores_rec, agree_rec, cost_rec, dis_rec):
        rec.close()

    plots.box({"%s/%s" % (a[:4], b[:4]): v for (a, b), v in agreement_by_pair.items()},
              "Spearman correlation",
              "How much do the measures agree? (across %d graphs)" % len(GRAPHS),
              os.path.join(charts, "agreement_by_pair.png"))

    print("\n" + "=" * 74)
    print("  Done. Files in %s" % outdir)
    print("=" * 74)
    print("\n  The pair that agreed most and least, averaged over %d graphs:"
          % len(GRAPHS))
    means = {p: sum(v) / len(v) for p, v in agreement_by_pair.items()}
    hi = max(means, key=means.get)
    lo = min(means, key=means.get)
    print("     most  agreement: %-12s vs %-12s  mean rho = %+.3f"
          % (hi[0], hi[1], means[hi]))
    print("     least agreement: %-12s vs %-12s  mean rho = %+.3f"
          % (lo[0], lo[1], means[lo]))
    print("\n  Now open disagreements.csv and look at the actual nodes.")
    print("  A correlation is a summary; the memo needs a named example.")


if __name__ == "__main__":
    main()
