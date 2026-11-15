"""Part 4 - does how you select the graph change the answer?

    python part-4/run_part4.py --who <your-name>

Takes the two two-sided graphs and runs the same algorithms three ways:
  (a) on the raw two-sided graph, as stored
  (b) projected onto side 0
  (c) projected onto side 1

then compares what each says about the SAME entities.

Writes into your-work/<your-name>/part4/:

    projection_shape.csv      what projection does to the size of the graph
    projection_mass.csv       where PageRank score piles up in the raw graph
    projection_rankings.csv   every entity's rank, raw vs projected
    projection_effect.csv     the comparison, one row per graph
    charts/*.png

About 30 seconds.
"""

from __future__ import annotations

import argparse
import os
import sys
import time

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "00-base")
sys.path.insert(0, BASE)

import networkx as nx  # noqa: E402
from networkx.algorithms import bipartite  # noqa: E402

from gdslab import loaders, plots, runs, stats  # noqa: E402

GRAPHS = ["crime", "unicodelang"]
SEEDS = 20

SHAPE_FIELDS = ["graph", "view", "nodes", "edges", "blowup_vs_raw",
                "away_side_max_degree", "biggest_single_contribution",
                "project_s"]
MASS_FIELDS = ["graph", "side", "n_nodes", "share_of_nodes",
               "share_of_pagerank", "mass_ratio"]
RANK_FIELDS = ["graph", "node", "side", "raw_pagerank", "raw_rank",
               "projected_pagerank", "projected_rank", "rank_change"]
EFFECT_FIELDS = ["graph", "side", "n_entities", "top10_overlap",
                 "top20_overlap", "spearman_raw_vs_projected",
                 "raw_communities", "projected_communities",
                 "ari_raw_vs_projected"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", required=True)
    args = ap.parse_args()

    outdir = os.path.join(BASE, "your-work", args.who, "part4")
    charts = os.path.join(outdir, "charts")
    os.makedirs(charts, exist_ok=True)

    info = runs.provenance()
    print("=" * 74)
    print("  Part 4 - does projection change the answer?")
    print("=" * 74)
    print("  machine : %s | %s cores\n" % (info["platform"], info["cpu_count"]))
    started = time.time()
    overlap_labels, overlap_values = [], []
    blowup_labels, blowup_values = [], []
    mass_labels, mass_values = [], []

    shape = runs.Recorder(os.path.join(outdir, "projection_shape.csv"), SHAPE_FIELDS)
    mass = runs.Recorder(os.path.join(outdir, "projection_mass.csv"), MASS_FIELDS)
    rank = runs.Recorder(os.path.join(outdir, "projection_rankings.csv"), RANK_FIELDS)
    effect = runs.Recorder(os.path.join(outdir, "projection_effect.csv"), EFFECT_FIELDS)

    for name in GRAPHS:
        G = loaders.load(name, weighted=False)
        sides = loaders.sides(name)
        side_nodes = {0: [n for n in G if sides[n] == 0],
                      1: [n for n in G if sides[n] == 1]}
        raw_edges = G.number_of_edges()
        print("  %s  (N=%d, E=%d, sides %d/%d)"
              % (name, G.number_of_nodes(), raw_edges,
                 len(side_nodes[0]), len(side_nodes[1])))

        shape.row(graph=name, view="raw (two-sided)", nodes=G.number_of_nodes(),
                  edges=raw_edges, blowup_vs_raw=1.0, away_side_max_degree="",
                  biggest_single_contribution="", project_s=0.0)

        # --- 1. where does score pile up in the RAW graph? ---------------
        raw_pr = nx.pagerank(G)
        for side in (0, 1):
            nodes = side_nodes[side]
            share_nodes = len(nodes) / G.number_of_nodes()
            share_pr = sum(raw_pr[n] for n in nodes)
            mass.row(graph=name, side=side, n_nodes=len(nodes),
                     share_of_nodes=round(share_nodes, 6),
                     share_of_pagerank=round(share_pr, 6),
                     mass_ratio=round(share_pr / share_nodes, 4))
            print("     raw PageRank: side %d holds %.1f%% of nodes but %.1f%% "
                  "of the score  (%.2fx)"
                  % (side, 100 * share_nodes, 100 * share_pr,
                     share_pr / share_nodes))
            mass_labels.append("%s s%d" % (name, side))
            mass_values.append(share_pr / share_nodes)

        raw_comms = nx.community.louvain_communities(G, seed=0)

        # --- 2. project each way and compare -----------------------------
        for side in (0, 1):
            keep = side_nodes[side]
            away = side_nodes[1 - side]
            t0 = time.perf_counter()
            P = bipartite.projected_graph(G, keep)
            project_s = time.perf_counter() - t0

            away_max = max(G.degree(n) for n in away)
            shape.row(graph=name, view="projected onto side %d" % side,
                      nodes=P.number_of_nodes(), edges=P.number_of_edges(),
                      blowup_vs_raw=round(P.number_of_edges() / raw_edges, 3),
                      away_side_max_degree=away_max,
                      biggest_single_contribution=away_max * (away_max - 1) // 2,
                      project_s=round(project_s, 4))
            print("     project onto side %d: %d -> %d edges (%.1fx)  "
                  "[biggest away-node has degree %d, contributing %d edges]"
                  % (side, raw_edges, P.number_of_edges(),
                     P.number_of_edges() / raw_edges, away_max,
                     away_max * (away_max - 1) // 2))

            proj_pr = nx.pagerank(P)

            def ranked(scores, universe):
                order = sorted(universe, key=lambda k: (-scores.get(k, 0), str(k)))
                return {k: i + 1 for i, k in enumerate(order)}

            raw_only = {n: raw_pr[n] for n in keep}
            r_raw, r_proj = ranked(raw_only, keep), ranked(proj_pr, keep)
            for node in sorted(keep):
                rank.row(graph=name, node=node, side=side,
                         raw_pagerank=round(raw_pr[node], 10),
                         raw_rank=r_raw[node],
                         projected_pagerank=round(proj_pr.get(node, 0.0), 10),
                         projected_rank=r_proj[node],
                         rank_change=r_raw[node] - r_proj[node])

            proj_comms = nx.community.louvain_communities(P, seed=0)
            raw_labels = {n: i for i, c in enumerate(raw_comms)
                          for n in c if n in set(keep)}
            proj_labels = {n: i for i, c in enumerate(proj_comms) for n in c}
            shared = set(raw_labels) & set(proj_labels)

            effect.row(
                graph=name, side=side, n_entities=len(keep),
                top10_overlap=round(stats.top_k_overlap(raw_only, proj_pr, 10), 4),
                top20_overlap=round(stats.top_k_overlap(raw_only, proj_pr, 20), 4),
                spearman_raw_vs_projected=round(stats.spearman(raw_only, proj_pr), 4),
                raw_communities=len(raw_comms),
                projected_communities=len(proj_comms),
                ari_raw_vs_projected=round(stats.adjusted_rand(
                    {k: raw_labels[k] for k in shared},
                    {k: proj_labels[k] for k in shared}), 4) if shared else "")
            print("        top-10 overlap raw vs projected: %.2f   spearman %+.3f"
                  % (stats.top_k_overlap(raw_only, proj_pr, 10),
                     stats.spearman(raw_only, proj_pr)))
            overlap_labels.append("%s s%d" % (name, side))
            overlap_values.append(stats.top_k_overlap(raw_only, proj_pr, 10))
            blowup_labels.append("%s s%d" % (name, side))
            blowup_values.append(P.number_of_edges() / raw_edges)
        print()

    for rec in (shape, mass, rank, effect):
        rec.close()

    plots.bar(overlap_labels, overlap_values,
              "top-10 overlap, raw vs projected",
              "How much does the top ten survive projection? (1.0 = unchanged)",
              os.path.join(charts, "top10_survival.png"))
    plots.bar(blowup_labels, blowup_values, "projected edges / raw edges",
              "How much does projection inflate the graph?",
              os.path.join(charts, "projection_blowup.png"))
    plots.bar(mass_labels, mass_values, "share of score / share of nodes",
              "Does one side accumulate score in the raw graph? (1.0 = neither)",
              os.path.join(charts, "score_mass_by_side.png"))

    print("=" * 74)
    print("  Done in %.0f s. Files in %s" % (time.time() - started, outdir))
    print("=" * 74)
    print("\n  The question is not 'which is right'. Both are correct")
    print("  computations. The question is which one ANSWERS what you asked.")


if __name__ == "__main__":
    main()
